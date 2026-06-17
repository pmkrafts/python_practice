"""Base agent interface."""

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    name: str = "base-agent"

    @abstractmethod
    async def run(self, user_input: str, **kwargs: Any) -> dict[str, Any]:
        """Run the agent with the given input.

        Args:
            user_input: The user's request or query.
            **kwargs: Additional runtime parameters.

        Returns:
            A dictionary containing the agent output.
        """

    async def stream(self, user_input: str, **kwargs: Any):
        """Optionally stream agent output tokens."""
        result = await self.run(user_input, **kwargs)
        yield result.get("output", "")
