"""Memory system for storing reasoning, feedback, and scores."""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from .agent import AgentResponse


@dataclass
class ReasoningEntry:
    """Single reasoning entry in memory."""
    timestamp: datetime
    user_input: str
    agent_responses: List[Dict[str, Any]]
    final_decision: Optional[str] = None
    user_feedback: Optional[str] = None
    loop_count: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MemoryStore:
    """Simple file-based memory store for MVP-0."""
    
    def __init__(self, memory_file: str = "data/memory.jsonl"):
        """
        Initialize memory store.
        
        Args:
            memory_file: Path to JSONL file for storing entries
        """
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self._entries: List[ReasoningEntry] = []
        self._load()
    
    def _load(self):
        """Load existing entries from file."""
        if not self.memory_file.exists():
            return
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        # Convert timestamp string back to datetime
                        if 'timestamp' in data:
                            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                        entry = ReasoningEntry(**data)
                        self._entries.append(entry)
        except Exception as e:
            print(f"Warning: Could not load memory: {e}")
    
    def save(self, entry: ReasoningEntry):
        """Save a reasoning entry to memory."""
        self._entries.append(entry)
        
        # Append to JSONL file
        try:
            with open(self.memory_file, 'a', encoding='utf-8') as f:
                # Convert to dict and handle datetime serialization
                entry_dict = asdict(entry)
                entry_dict['timestamp'] = entry.timestamp.isoformat()
                # agent_responses should already be dicts from orchestrator
                f.write(json.dumps(entry_dict, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Warning: Could not save to memory: {e}")
    
    def get_recent_entries(self, limit: int = 10) -> List[ReasoningEntry]:
        """Get recent reasoning entries."""
        return self._entries[-limit:]
    
    def get_user_history(self, user_input_pattern: Optional[str] = None) -> List[ReasoningEntry]:
        """Get entries matching user input pattern."""
        if not user_input_pattern:
            return self._entries
        
        pattern_lower = user_input_pattern.lower()
        return [
            entry for entry in self._entries
            if pattern_lower in entry.user_input.lower()
        ]
    
    def get_agent_preferences(self, agent_name: str) -> Dict[str, Any]:
        """
        Get user preference scores for an agent based on feedback history.
        Returns dict with preference score and interaction count.
        """
        positive_count = 0
        total_count = 0
        
        for entry in self._entries:
            if entry.user_feedback:
                # Check if this agent's response was accepted
                for resp in entry.agent_responses:
                    if resp.get('agent_name') == agent_name:
                        total_count += 1
                        # Simple heuristic: if final_decision mentions agent, it's positive
                        if entry.final_decision and agent_name.lower() in entry.final_decision.lower():
                            positive_count += 1
        
        if total_count == 0:
            return {"preference_score": 0.5, "interaction_count": 0}
        
        preference_score = positive_count / total_count
        return {
            "preference_score": preference_score,
            "interaction_count": total_count,
            "positive_count": positive_count
        }
    
    def clear(self):
        """Clear all memory (use with caution)."""
        self._entries = []
        if self.memory_file.exists():
            self.memory_file.unlink()

