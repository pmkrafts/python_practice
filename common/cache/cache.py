"""Cache-aside decorator and helper."""

import functools
import json
from typing import Any, Callable

from common.cache.redis_client import get_redis


async def cache_get(key: str) -> Any | None:
    """Get a value from Redis cache."""
    client = await get_redis()
    value = await client.get(key)
    if value is None:
        return None
    return json.loads(value)


async def cache_set(key: str, value: Any, ttl: int = 60) -> None:
    """Set a value in Redis cache with TTL in seconds."""
    client = await get_redis()
    await client.setex(key, ttl, json.dumps(value))


async def cache_delete(key: str) -> None:
    """Delete a value from Redis cache."""
    client = await get_redis()
    await client.delete(key)


async def cache_delete_pattern(pattern: str) -> None:
    """Delete all keys matching a pattern."""
    client = await get_redis()
    keys = await client.keys(pattern)
    if keys:
        await client.delete(*keys)


def cached(
    key_prefix: str,
    ttl: int = 60,
    key_builder: Callable[..., str] | None = None,
) -> Callable:
    """Decorator that caches the result of an async function in Redis.

    Args:
        key_prefix: Prefix for the cache key.
        ttl: Time-to-live in seconds.
        key_builder: Optional function to build a custom cache key.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                key_parts = [key_prefix]
                for arg in args[1:] if len(args) > 1 and isinstance(args[0], object) else args:
                    key_parts.append(str(arg))
                for k, v in sorted(kwargs.items()):
                    key_parts.append(f"{k}={v}")
                cache_key = ":".join(key_parts)

            cached_value = await cache_get(cache_key)
            if cached_value is not None:
                return cached_value

            result = await func(*args, **kwargs)
            await cache_set(cache_key, result, ttl)
            return result

        return wrapper

    return decorator
