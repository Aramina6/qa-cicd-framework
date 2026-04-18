"""
tests/unit/core/test_data_models.py

Real-world enterprise unit tests for core data models.
These models are the foundation of every autonomous execution task and AI agent config
in the platform. They enforce strict validation at creation time to prevent bad data
from reaching the LLM orchestration layer.

Why these tests exist:
- Data validation is the #1 source of production bugs in AI platforms.
- Pydantic models give us type safety + runtime validation.
- These tests run in < 0.1s on every PR → instant feedback.
"""

import pytest
import uuid
from pydantic import ValidationError

# Import the actual source code we want to test
from src.core.models import ExecutionTask, AgentConfig


def test_execution_task_valid_creation_with_factory():
    """Test the recommended factory method (used everywhere in production code)."""
    task = ExecutionTask.create(
        prompt="Analyze quarterly revenue trends and generate executive summary",
        max_retries=5,
        timeout_seconds=45.0
    )
    
    assert isinstance(task.task_id, str)
    assert len(task.task_id) > 0
    assert task.prompt == "Analyze quarterly revenue trends and generate executive summary"
    assert task.max_retries == 5
    assert task.timeout_seconds == 45.0
    assert isinstance(task.metadata, dict)
    assert task.metadata == {}  # default value


def test_execution_task_auto_generated_uuid():
    """Ensure every task gets a unique UUID by default."""
    task1 = ExecutionTask.create("Task 1")
    task2 = ExecutionTask.create("Task 2")
    
    assert task1.task_id != task2.task_id
    assert uuid.UUID(task1.task_id)  # validates it's a real UUID


def test_execution_task_invalid_values_raise_validation_error():
    """Pydantic must reject clearly invalid data immediately."""
    with pytest.raises(ValidationError) as exc_info:
        ExecutionTask.create(
            prompt="Test task",
            max_retries=-1,           # negative retries not allowed
            timeout_seconds=-10.0     # negative timeout not allowed
        )
    
    # Check that both fields are mentioned in the error
    error_str = str(exc_info.value)
    assert "max_retries" in error_str
    assert "timeout_seconds" in error_str


def test_agent_config_valid_creation():
    """Happy path for agent configuration."""
    config = AgentConfig(
        agent_id="revenue_analyst_v1",
        tools=["sql_query", "data_visualizer", "email_sender"],
        temperature=0.3,
        system_prompt="You are a senior financial analyst. Be precise and concise."
    )
    
    assert config.agent_id == "revenue_analyst_v1"
    assert len(config.tools) == 3
    assert config.temperature == 0.3
    assert config.system_prompt is not None


def test_agent_config_default_values():
    """Verify sensible defaults that are used when creating agents quickly."""
    config = AgentConfig(agent_id="quick_agent")
    
    assert config.tools == []
    assert config.temperature == 0.7
    assert config.system_prompt is None


def test_agent_config_temperature_bounds_enforced():
    """Temperature must stay between 0.0 and 1.0 (critical for LLM behavior)."""
    # Valid edge cases
    AgentConfig(agent_id="agent_low", temperature=0.0)
    AgentConfig(agent_id="agent_high", temperature=1.0)
    
    # Invalid cases must raise
    with pytest.raises(ValidationError):
        AgentConfig(agent_id="agent_too_low", temperature=-0.1)
    
    with pytest.raises(ValidationError):
        AgentConfig(agent_id="agent_too_high", temperature=1.1)


def test_agent_config_empty_tools_allowed():
    """Some agents may not need tools initially – this is valid."""
    config = AgentConfig(agent_id="simple_chat_agent", tools=[])
    assert config.tools == []


# Optional: Property-based test using Hypothesis (extra robustness)
from hypothesis import given, strategies as st

@given(
    agent_id=st.text(min_size=3, max_size=50),
    temperature=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
)
def test_agent_config_property_based(agent_id, temperature):
    """Random valid inputs must always create a valid config."""
    config = AgentConfig(agent_id=agent_id, temperature=temperature)
    assert 0.0 <= config.temperature <= 1.0
