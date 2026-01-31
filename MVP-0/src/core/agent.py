"""Base Agent class for MINA multi-agent system."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import os
import google.generativeai as genai


@dataclass
class AgentResponse:
    """Response from an agent."""
    agent_name: str
    content: str
    reasoning: Optional[str] = None
    confidence: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentContext:
    """Context passed to agents during reasoning."""
    user_input: str
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    available_data: Dict[str, Any] = field(default_factory=dict)
    other_agents_responses: List[AgentResponse] = field(default_factory=list)
    loop_count: int = 0


class BaseAgent(ABC):
    """Base class for all agents in MINA system."""
    
    def __init__(self, name: str, persona_file: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize agent.
        
        Args:
            name: Agent name (e.g., "Mina", "Mila")
            persona_file: Path to persona markdown file (optional, can load from Drive)
            api_key: Gemini API key (optional, reads from env if not provided)
        """
        self.name = name
        self.persona_file = persona_file
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(f"GEMINI_API_KEY not found for agent {name}")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = None
        self.persona_instruction = ""
        
    def load_persona(self, instruction: str):
        """Load persona instruction (from file or Drive)."""
        self.persona_instruction = instruction
        # Initialize chat with persona
        self.chat = self.model.start_chat(history=[])
        self.chat.send_message(f"Hệ thống: Hãy đóng vai nhân cách này: {instruction}")
    
    @abstractmethod
    def get_role_description(self) -> str:
        """Return brief role description of this agent."""
        pass
    
    def reason(self, context: AgentContext) -> AgentResponse:
        """
        Main reasoning method - agents implement their specific logic here.
        
        Args:
            context: Current context with user input, history, data, etc.
            
        Returns:
            AgentResponse with agent's reasoning and conclusion
        """
        if not self.chat:
            raise RuntimeError(f"Agent {self.name} persona not loaded. Call load_persona() first.")
        
        # Build prompt from context
        prompt = self._build_prompt(context)
        
        try:
            # Get response from LLM
            response = self.chat.send_message(prompt)
            content = response.text
            
            # Extract reasoning if possible
            reasoning = self._extract_reasoning(content)
            
            return AgentResponse(
                agent_name=self.name,
                content=content,
                reasoning=reasoning,
                confidence=self._estimate_confidence(content, context),
                metadata={"loop_count": context.loop_count}
            )
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                content=f"Lỗi khi xử lý: {str(e)}",
                reasoning=None,
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    def _build_prompt(self, context: AgentContext) -> str:
        """Build prompt for LLM based on context."""
        prompt_parts = []
        
        # Add context about other agents' responses
        if context.other_agents_responses:
            prompt_parts.append("=== Phản hồi từ các agent khác ===")
            for resp in context.other_agents_responses:
                prompt_parts.append(f"\n{resp.agent_name}: {resp.content}")
            prompt_parts.append("\n")
        
        # Add available data
        if context.available_data:
            prompt_parts.append("=== Dữ liệu có sẵn ===")
            for key, value in context.available_data.items():
                prompt_parts.append(f"{key}: {value}")
            prompt_parts.append("\n")
        
        # Add conversation history
        if context.conversation_history:
            prompt_parts.append("=== Lịch sử hội thoại ===")
            for msg in context.conversation_history[-5:]:  # Last 5 messages
                prompt_parts.append(f"{msg.get('role', 'user')}: {msg.get('content', '')}")
            prompt_parts.append("\n")
        
        # Add current user input
        prompt_parts.append(f"=== Yêu cầu hiện tại ===")
        prompt_parts.append(context.user_input)
        prompt_parts.append("\n")
        prompt_parts.append("Hãy phân tích và đưa ra phản hồi theo vai trò của bạn.")
        
        return "\n".join(prompt_parts)
    
    def _extract_reasoning(self, content: str) -> Optional[str]:
        """Extract reasoning from response (can be overridden by subclasses)."""
        # Simple heuristic: look for reasoning markers
        if "lý do" in content.lower() or "vì" in content.lower():
            return content[:200]  # First 200 chars as reasoning
        return None
    
    def _estimate_confidence(self, content: str, context: AgentContext) -> float:
        """Estimate confidence level (0.0 to 1.0)."""
        # Simple heuristic: longer, more structured responses = higher confidence
        if len(content) < 50:
            return 0.3
        elif len(content) < 200:
            return 0.6
        else:
            return 0.8
    
    def can_refuse(self, context: AgentContext) -> bool:
        """
        Check if agent can refuse to answer (wait for other agents).
        Override in subclasses for specific logic.
        """
        return False
    
    def should_stop(self, context: AgentContext) -> bool:
        """
        Check if agent thinks reasoning should stop.
        Override in subclasses for specific logic.
        """
        return False

