from typing import Dict, Any, Callable

class ToolRegistry:
    """Registry of tools that agents can call. Core of autonomous execution."""
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.tools[name] = func

    def get_tool(self, name: str) -> Callable:
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        return self.tools[name]
