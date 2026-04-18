from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict, Any
import uuid

class ExecutionTask(BaseModel):
    """Represents a single autonomous execution task in the platform."""
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prompt: str
    max_retries: int = Field(default=3, ge=0)
    timeout_seconds: float = Field(default=30.0, gt=0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def create(cls, prompt: str, max_retries: int = 3, timeout_seconds: float = 30.0):
        """Factory method - used in real code to enforce validation at creation time."""
        return cls(prompt=prompt, max_retries=max_retries, timeout_seconds=timeout_seconds)

class AgentConfig(BaseModel):
    """Configuration for an AI agent/orchestrator."""
    agent_id: str
    tools: List[str] = Field(default_factory=list)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    system_prompt: Optional[str] = None
