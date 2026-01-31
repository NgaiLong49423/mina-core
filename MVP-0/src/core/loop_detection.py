"""Loop detection mechanism for reasoning cycles."""

from typing import List, Dict, Any
from .agent import AgentResponse
from collections import deque


class LoopDetector:
    """Detect reasoning loops in agent responses."""
    
    def __init__(self, max_history: int = 5, similarity_threshold: float = 0.8):
        """
        Initialize loop detector.
        
        Args:
            max_history: Number of recent responses to check
            similarity_threshold: Similarity threshold (0.0-1.0) to consider as loop
        """
        self.max_history = max_history
        self.similarity_threshold = similarity_threshold
        self.response_history: deque = deque(maxlen=max_history)
        self.loop_count: Dict[str, int] = {}  # Track loop count per agent
    
    def check_loop(self, responses: List[AgentResponse]) -> Dict[str, Any]:
        """
        Check if current responses indicate a loop.
        
        Args:
            responses: Current round of agent responses
            
        Returns:
            Dict with loop detection results:
            - is_loop: bool
            - loop_agents: List of agent names in loop
            - loop_count: int
            - recommendation: str (what to do)
        """
        # Convert responses to simple representation for comparison
        current_round = self._normalize_responses(responses)
        
        # Check against history
        loop_found = False
        loop_agents = []
        
        for hist_round in self.response_history:
            similarity = self._calculate_similarity(current_round, hist_round)
            if similarity >= self.similarity_threshold:
                loop_found = True
                # Find which agents are repeating
                for agent_name, content in current_round.items():
                    if agent_name in hist_round:
                        if self._text_similarity(content, hist_round[agent_name]) >= 0.7:
                            loop_agents.append(agent_name)
                break
        
        # Update loop counts
        if loop_found:
            for agent_name in loop_agents:
                self.loop_count[agent_name] = self.loop_count.get(agent_name, 0) + 1
        
        # Add current round to history
        self.response_history.append(current_round)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(loop_found, loop_agents)
        
        return {
            "is_loop": loop_found,
            "loop_agents": list(set(loop_agents)),
            "loop_count": sum(self.loop_count.values()),
            "recommendation": recommendation,
            "agent_loop_counts": self.loop_count.copy()
        }
    
    def _normalize_responses(self, responses: List[AgentResponse]) -> Dict[str, str]:
        """Normalize responses to simple dict for comparison."""
        normalized = {}
        for resp in responses:
            # Take first 200 chars and normalize
            content = resp.content[:200].lower().strip()
            normalized[resp.agent_name] = content
        return normalized
    
    def _calculate_similarity(self, round1: Dict[str, str], round2: Dict[str, str]) -> float:
        """Calculate similarity between two rounds of responses."""
        if not round1 or not round2:
            return 0.0
        
        # Check overlap of agents
        common_agents = set(round1.keys()) & set(round2.keys())
        if not common_agents:
            return 0.0
        
        # Calculate average text similarity for common agents
        similarities = []
        for agent in common_agents:
            sim = self._text_similarity(round1[agent], round2[agent])
            similarities.append(sim)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Simple text similarity using word overlap."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def _generate_recommendation(self, is_loop: bool, loop_agents: List[str]) -> str:
        """Generate recommendation based on loop detection."""
        if not is_loop:
            return "Tiếp tục reasoning bình thường."
        
        if len(loop_agents) == 1:
            return f"Phát hiện vòng lặp từ {loop_agents[0]}. Nên giảm độ ưu tiên hoặc yêu cầu agent khác trả lời trước."
        elif len(loop_agents) >= 2:
            return f"Phát hiện vòng lặp từ nhiều agents: {', '.join(loop_agents)}. Cần thay đổi chiến lược hoặc yêu cầu User can thiệp."
        else:
            return "Phát hiện vòng lặp. Cần thay đổi chiến lược reasoning."
    
    def reset(self):
        """Reset loop detection state."""
        self.response_history.clear()
        self.loop_count.clear()
    
    def get_agent_priority_adjustment(self, agent_name: str) -> float:
        """
        Get priority adjustment for an agent based on loop count.
        Returns multiplier (0.0-1.0) - lower means lower priority.
        """
        loop_count = self.loop_count.get(agent_name, 0)
        if loop_count == 0:
            return 1.0
        elif loop_count == 1:
            return 0.7
        elif loop_count == 2:
            return 0.4
        else:
            return 0.1  # Very low priority after 3+ loops

