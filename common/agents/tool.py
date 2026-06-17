"""Dynamic tool registry and decorator."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Tool:
    """Represents a callable tool exposed to agents."""

    name: str
    description: str
    func: Callable[..., Any]
    parameters: dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    """Registry for agent tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        func: Callable[..., Any] | None = None,
        *,
        name: str | None = None,
        description: str | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> Callable:
        """Register a function as an agent tool.

        Can be used as a decorator or a direct function call.
        """

        def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
            tool_name = name or f.__name__
            tool_description = description or (f.__doc__ or "").strip()
            self._tools[tool_name] = Tool(
                name=tool_name,
                description=tool_description,
                func=f,
                parameters=parameters or {},
            )
            return f

        if func is not None:
            return decorator(func)
        return decorator

    def get(self, name: str) -> Tool:
        """Retrieve a tool by name."""
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found")
        return self._tools[name]

    def list_tools(self) -> list[Tool]:
        """Return all registered tools."""
        return list(self._tools.values())

    def clear(self) -> None:
        """Remove all tools from the registry."""
        self._tools.clear()


# Global registry instance
tool_registry = ToolRegistry()


def tool(
    func: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    parameters: dict[str, Any] | None = None,
) -> Callable:
    """Decorator to register a function as an agent tool."""
    return tool_registry.register(
        func,
        name=name,
        description=description,
        parameters=parameters,
    )


def invoke_tool(name: str, **kwargs: Any) -> Any:
    """Invoke a registered tool by name."""
    registered = tool_registry.get(name)
    return registered.func(**kwargs)
