"""Mina Core Orchestrator - coordinates multi-agent reasoning."""

from typing import List, Dict, Any, Optional
from .agent import BaseAgent, AgentContext, AgentResponse
from .agents import MinaAgent, MilaAgent, MisaAgent, MitaAgent
from .memory import MemoryStore
from .loop_detection import LoopDetector
from datetime import datetime


class MinaCoreOrchestrator:
    """Core orchestrator for MINA multi-agent reasoning system."""
    
    def __init__(
        self,
        memory_file: str = "data/memory.jsonl",
        max_loops: int = 5,
        api_key: Optional[str] = None
    ):
        """
        Initialize orchestrator.
        
        Args:
            memory_file: Path to memory storage file
            max_loops: Maximum reasoning loops before requiring human intervention
            api_key: Gemini API key (optional, reads from env)
        """
        self.memory = MemoryStore(memory_file)
        self.loop_detector = LoopDetector()
        self.max_loops = max_loops
        self.api_key = api_key
        
        # Initialize agents (persona will be loaded later)
        self.agents: Dict[str, BaseAgent] = {
            "Mina": MinaAgent(api_key=api_key),
            "Mila": MilaAgent(api_key=api_key),
            "Misa": MisaAgent(api_key=api_key),
            "Mita": MitaAgent(api_key=api_key)
        }
        
        # Agent priorities (can be adjusted based on user preferences)
        self.agent_priorities: Dict[str, float] = {
            "Mina": 1.0,
            "Mila": 1.0,
            "Misa": 1.0,
            "Mita": 1.0
        }
        
        self.conversation_history: List[Dict[str, str]] = []
    
    def load_agent_personas(self, persona_instructions: Dict[str, str]):
        """
        Load persona instructions for agents.
        
        Args:
            persona_instructions: Dict mapping agent name to persona instruction text
        """
        for agent_name, instruction in persona_instructions.items():
            if agent_name in self.agents:
                self.agents[agent_name].load_persona(instruction)
    
    def reason(
        self,
        user_input: str,
        available_data: Optional[Dict[str, Any]] = None,
        user_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Main reasoning method - coordinates multi-agent reasoning.
        
        Args:
            user_input: User's input/question
            available_data: Available data from Mina Core (facts, context)
            user_mode: True if user is actively participating (Yes-User mode)
            
        Returns:
            Dict with reasoning results:
            - responses: List of agent responses
            - summary: Summary of all responses
            - loop_detection: Loop detection results
            - requires_user_input: Whether user intervention is needed
        """
        if available_data is None:
            available_data = {}
        
        # Add user input to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        loop_count = 0
        all_responses: List[AgentResponse] = []
        
        while loop_count < self.max_loops:
            # Build context for this round
            context = AgentContext(
                user_input=user_input,
                conversation_history=self.conversation_history,
                available_data=available_data,
                other_agents_responses=all_responses[-len(self.agents):] if all_responses else [],
                loop_count=loop_count
            )
            
            # Get responses from all agents (in priority order)
            round_responses: List[AgentResponse] = []
            agent_order = self._get_agent_order()
            
            for agent_name in agent_order:
                agent = self.agents[agent_name]
                
                # Check if agent can refuse
                if agent.can_refuse(context):
                    continue
                
                # Get response
                response = agent.reason(context)
                round_responses.append(response)
                all_responses.append(response)
            
            # Check for loops
            loop_info = self.loop_detector.check_loop(round_responses)
            
            # Adjust priorities based on loop detection
            if loop_info["is_loop"]:
                for agent_name in loop_info["loop_agents"]:
                    adjustment = self.loop_detector.get_agent_priority_adjustment(agent_name)
                    self.agent_priorities[agent_name] *= adjustment
            
            # Check if we should stop
            should_stop = self._should_stop(round_responses, loop_info, user_mode)
            
            if should_stop:
                break
            
            loop_count += 1
            
            # In Yes-User mode, ask user after first round
            if user_mode and loop_count == 1:
                break
        
        # Generate summary
        summary = self._generate_summary(all_responses)
        
        # Save to memory
        from .memory import ReasoningEntry
        entry = ReasoningEntry(
            timestamp=datetime.now(),
            user_input=user_input,
            agent_responses=[self._response_to_dict(r) for r in all_responses],
            loop_count=loop_count,
            metadata={"user_mode": user_mode}
        )
        self.memory.save(entry)
        
        return {
            "responses": [self._response_to_dict(r) for r in all_responses],
            "summary": summary,
            "loop_detection": loop_info,
            "loop_count": loop_count,
            "requires_user_input": loop_count >= self.max_loops or loop_info["is_loop"],
            "agent_order": agent_order
        }
    
    def _get_agent_order(self) -> List[str]:
        """Get agent order based on priorities."""
        # Sort by priority (higher first)
        sorted_agents = sorted(
            self.agent_priorities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [name for name, _ in sorted_agents]
    
    def _should_stop(
        self,
        responses: List[AgentResponse],
        loop_info: Dict[str, Any],
        user_mode: bool
    ) -> bool:
        """Determine if reasoning should stop."""
        # Stop if loop detected and not in user mode
        if loop_info["is_loop"] and not user_mode:
            return True
        
        # Stop if all agents agree (simple heuristic: similar responses)
        if len(responses) >= 2:
            contents = [r.content.lower()[:100] for r in responses]
            if len(set(contents)) == 1:  # All same
                return True
        
        return False
    
    def _generate_summary(self, responses: List[AgentResponse]) -> str:
        """Generate summary of all agent responses."""
        if not responses:
            return "Không có phản hồi từ agents."
        
        summary_parts = []
        summary_parts.append("=== Tổng hợp phản hồi từ các agents ===\n")
        
        for resp in responses:
            summary_parts.append(f"{resp.agent_name}: {resp.content[:200]}...")
        
        return "\n".join(summary_parts)
    
    def _response_to_dict(self, response: AgentResponse) -> Dict[str, Any]:
        """Convert AgentResponse to dict for storage."""
        return {
            "agent_name": response.agent_name,
            "content": response.content,
            "reasoning": response.reasoning,
            "confidence": response.confidence,
            "timestamp": response.timestamp.isoformat(),
            "metadata": response.metadata
        }
    
    def add_user_feedback(self, reasoning_id: Optional[str] = None, feedback: str = ""):
        """Add user feedback to the last reasoning entry."""
        # For MVP-0, we'll update the most recent entry
        recent = self.memory.get_recent_entries(limit=1)
        if recent:
            recent[0].user_feedback = feedback
            # Update preference scores
            # (In full implementation, would update the stored entry)
    
    def update_agent_priorities_from_memory(self):
        """Update agent priorities based on user preference history."""
        for agent_name in self.agents.keys():
            prefs = self.memory.get_agent_preferences(agent_name)
            # Adjust priority based on preference score
            base_priority = 1.0
            if prefs["interaction_count"] > 0:
                # Higher preference = higher priority
                self.agent_priorities[agent_name] = base_priority * prefs["preference_score"]

