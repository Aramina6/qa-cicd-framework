"""
tests/unit/ai_orchestration/test_tools.py

Unit tests for the ToolRegistry — the core of autonomous agent execution.
Agents must be able to discover and call tools reliably. Any bug here would
break the entire "autonomous execution" promise of the platform.
"""

import pytest
from src.ai_orchestration.tools import ToolRegistry


def dummy_revenue_tool(month: str) -> dict:
    """Dummy tool used only for testing."""
    return {"month": month, "revenue": 14800000}


def test_tool_registry_register_and_get():
    """Register a tool and retrieve it successfully."""
    registry = ToolRegistry()
    registry.register("get_revenue", dummy_revenue_tool)
    
    tool = registry.get_tool("get_revenue")
    assert tool is dummy_revenue_tool
    assert tool("2026-03") == {"month": "2026-03", "revenue": 14800000}


def test_tool_registry_raises_on_missing_tool():
    """Requesting a non-existent tool must raise clear error."""
    registry = ToolRegistry()
    
    with pytest.raises(ValueError) as exc_info:
        registry.get_tool("non_existent_tool")
    
    assert "Tool 'non_existent_tool' not found" in str(exc_info.value)


def test_tool_registry_multiple_tools():
    """Register many tools — all must be retrievable."""
    registry = ToolRegistry()
    registry.register("get_revenue", dummy_revenue_tool)
    registry.register("send_email", lambda x: "email sent")
    
    assert registry.get_tool("get_revenue") is dummy_revenue_tool
    assert registry.get_tool("send_email")("test") == "email sent"
