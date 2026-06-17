"""Async Redis client wrapper."""

import redis.asyncio as redis

from common.core.config import settings

_redis_client: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    """Return a shared async Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
    return _redis_client


async def close_redis() -> None:
    """Close the shared Redis connection."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
