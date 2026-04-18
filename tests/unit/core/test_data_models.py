import pytest
from pydantic import ValidationError
# Assume you have these models in src/core/models.py
# from src.core.models import ExecutionTask, AgentConfig

# For now we'll define minimal models here for demonstration
from pydantic import BaseModel, Field
from typing import List, Optional

class ExecutionTask(BaseModel):
    task_id: str
    prompt: str
    max_retries: int = Field(default=3, ge=0)
    timeout_seconds: float = Field(default=30.0, gt=0)

class AgentConfig(BaseModel):
    agent_id: str
    tools: List[str]
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

def test_execution_task_valid_creation():
    task = ExecutionTask(task_id="task_001", prompt="Analyze revenue data")
    assert task.task_id == "task_001"
    assert task.max_retries == 3

def test_execution_task_invalid_timeout():
    with pytest.raises(ValidationError):
        ExecutionTask(task_id="task_002", prompt="Test", timeout_seconds=-5)

def test_agent_config_temperature_bounds():
    config = AgentConfig(agent_id="agent_1", tools=["calculator"])
    assert 0.0 <= config.temperature <= 1.0

    with pytest.raises(ValidationError):
        AgentConfig(agent_id="agent_2", tools=[], temperature=1.5)
