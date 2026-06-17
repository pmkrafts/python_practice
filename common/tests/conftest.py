"""Shared pytest fixtures."""

import pytest
import pytest_asyncio


@pytest.fixture
def anyio_backend() -> str:
    """Set the anyio backend for async tests."""
    return "asyncio"


@pytest_asyncio.fixture
async def redis_client():
    """Provide an async Redis client for tests."""
    from common.cache.redis_client import get_redis, close_redis

    client = await get_redis()
    try:
        yield client
    finally:
        await client.flushdb()
        await close_redis()


@pytest.fixture
def sample_chat_history() -> list[dict[str, str]]:
    """Return a sample chat history for memory/agent tests."""
    return [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]
