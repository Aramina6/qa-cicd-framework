"""
tests/unit/ai_orchestration/test_prompt_utils.py

Real-world unit tests for prompt formatting utilities.
Prompt formatting is critical because LLMs are extremely sensitive to missing variables,
wrong syntax, or malformed templates — one small bug can cause complete failure of
autonomous execution flows.
"""

import pytest
from hypothesis import given, strategies as st

# Import the actual production code we are testing
from src.ai_orchestration.prompt_utils import format_prompt


def test_format_prompt_success_with_all_variables():
    """Happy path: all variables present → should format correctly."""
    template = "Hello {name}, your Q1 revenue is {revenue}."
    variables = {"name": "Alice", "revenue": "$14.8M"}
    
    result = format_prompt(template, variables)
    assert result == "Hello Alice, your Q1 revenue is $14.8M."


def test_format_prompt_raises_on_missing_variable():
    """Critical safety check: missing variable must raise clear error."""
    template = "Revenue for {region} is {amount}."
    variables = {"region": "Enterprise"}  # missing "amount"
    
    with pytest.raises(ValueError) as exc_info:
        format_prompt(template, variables)
    
    assert "Missing variable in prompt template: 'amount'" in str(exc_info.value)


def test_format_prompt_handles_empty_variables_dict():
    """Edge case: no variables provided."""
    template = "This is a static prompt with no variables."
    result = format_prompt(template, {})
    assert result == template


def test_format_prompt_ignores_extra_variables():
    """Extra variables in dict should be safely ignored (not an error)."""
    template = "Hello {name}."
    variables = {"name": "Bob", "extra_key": "ignored_value"}
    result = format_prompt(template, variables)
    assert result == "Hello Bob."


# Property-based test (tests thousands of random valid cases automatically)
@given(
    template=st.text(min_size=10, max_size=300),
    var_name=st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_", min_size=3, max_size=20),
    var_value=st.text(max_size=100)
)
def test_prompt_formatting_property_based(template, var_name, var_value):
    """Random valid inputs must always succeed if the variable is present."""
    # Only test when the variable actually appears in the template
    if "{" + var_name + "}" in template:
        variables = {var_name: var_value}
        result = format_prompt(template, variables)
        assert var_value in result
