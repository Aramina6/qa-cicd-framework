def format_prompt(template: str, variables: dict) -> str:
    """Safely format prompt templates with variables. Critical for LLM reliability."""
    try:
        return template.format(**variables)
    except KeyError as e:
        raise ValueError(f"Missing variable in prompt template: {e}") from e
