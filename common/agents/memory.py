"""Agent memory interfaces and implementations."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Message:
    """A single conversation message."""

    role: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseMemory(ABC):
    """Abstract interface for agent memory."""

    @abstractmethod
    async def add(self, message: Message) -> None:
        """Add a message to memory."""

    @abstractmethod
    async def get(self, limit: int = 10) -> list[Message]:
        """Retrieve recent messages."""

    @abstractmethod
    async def clear(self) -> None:
        """Clear all memory."""


class ConversationMemory(BaseMemory):
    """In-memory conversation buffer."""

    def __init__(self, max_messages: int = 20) -> None:
        self._messages: list[Message] = []
        self._max_messages = max_messages

    async def add(self, message: Message) -> None:
        self._messages.append(message)
        if len(self._messages) > self._max_messages:
            self._messages = self._messages[-self._max_messages :]

    async def get(self, limit: int = 10) -> list[Message]:
        return self._messages[-limit:]

    async def clear(self) -> None:
        self._messages.clear()

    async def summarize(self, summarizer: Callable[[list[Message]], str]) -> str:
        """Return a summary of the conversation using a provided summarizer."""
        return summarizer(self._messages)
