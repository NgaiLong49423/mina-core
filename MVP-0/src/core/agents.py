"""Specific agent implementations: Mina, Mila, Misa, Mita."""

from typing import Optional
from .agent import BaseAgent, AgentContext, AgentResponse


class MinaAgent(BaseAgent):
    """Mina - Logic/Reality agent."""
    
    def __init__(self, persona_file: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__("Mina", persona_file, api_key)
    
    def get_role_description(self) -> str:
        return "Thực tế / logic - Đề xuất phương án dựa trên dữ liệu ban đầu; cảm xúc bằng không."
    
    def can_refuse(self, context: AgentContext) -> bool:
        # Mina can refuse if waiting for emotional context from Mita
        if context.other_agents_responses:
            mita_responses = [r for r in context.other_agents_responses if r.agent_name == "Mita"]
            if not mita_responses and "cảm xúc" in context.user_input.lower():
                return True
        return False
    
    def _build_prompt(self, context: AgentContext) -> str:
        base_prompt = super()._build_prompt(context)
        return f"{base_prompt}\n\nLưu ý: Bạn là Mina - tập trung vào logic và dữ liệu thực tế. Không thêm cảm xúc."


class MilaAgent(BaseAgent):
    """Mila - Practical/Discipline agent."""
    
    def __init__(self, persona_file: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__("Mila", persona_file, api_key)
    
    def get_role_description(self) -> str:
        return "Thực dụng / hành động - Đánh giá phương án, ưu tiên lợi ích và hành động."
    
    def _build_prompt(self, context: AgentContext) -> str:
        base_prompt = super()._build_prompt(context)
        return f"{base_prompt}\n\nLưu ý: Bạn là Mila - kỷ luật và thực dụng. Ưu tiên hành động cụ thể và deadline."


class MisaAgent(BaseAgent):
    """Misa - Philosophy/Critical Thinking agent."""
    
    def __init__(self, persona_file: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__("Misa", persona_file, api_key)
    
    def get_role_description(self) -> str:
        return "Triết lý / hậu quả - Phân tích sâu về hậu quả, khác biệt giữa lý thuyết và thực tế."
    
    def _build_prompt(self, context: AgentContext) -> str:
        base_prompt = super()._build_prompt(context)
        return f"{base_prompt}\n\nLưu ý: Bạn là Misa - tư duy phản biện và triết học. Mổ xẻ logic và chỉ ra giả định."


class MitaAgent(BaseAgent):
    """Mita - Empathy/Emotional agent."""
    
    def __init__(self, persona_file: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__("Mita", persona_file, api_key)
    
    def get_role_description(self) -> str:
        return "Thấu cảm / cảm xúc - Đánh giá góc nhìn cảm xúc của người dùng; cân nhắc cái giá phải trả và hậu quả cảm xúc."
    
    def _build_prompt(self, context: AgentContext) -> str:
        base_prompt = super()._build_prompt(context)
        return f"{base_prompt}\n\nLưu ý: Bạn là Mita - thấu cảm nhưng thực tế. Nhận diện cảm xúc và kéo về thực tế."

