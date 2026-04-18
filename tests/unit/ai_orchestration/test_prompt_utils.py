import pytest
from hypothesis import given, strategies as st

# Example function we'll test (create this in src/ai_orchestration/prompt_utils.py later)
def format_prompt(template: str, variables: dict) -> str:
    """Safely format prompt with variables"""
    try:
        return template.format(**variables)
    except KeyError as e:
        raise ValueError(f"Missing variable in prompt template: {e}")

@given(
    template=st.text(min_size=5, max_size=200),
    var_name=st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=3, max_size=10)
)
def test_prompt_formatting_with_variables(template, var_name):
    if "{" + var_name + "}" in template:
        variables = {var_name: "test_value"}
        result = format_prompt(template, variables)
        assert var_name in result or "test_value" in result
    else:
        # Should raise if required var missing - but we skip for this property test
        pass

def test_format_prompt_missing_variable():
    template = "Hello {name}, your revenue is {revenue}"
    with pytest.raises(ValueError, match="Missing variable"):
        format_prompt(template, {"name": "Alice"})
