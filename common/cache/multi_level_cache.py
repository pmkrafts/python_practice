"""Multi-level cache: in-memory LRU + Redis fallback."""

import functools
import json
from collections import OrderedDict
from typing import Any, Callable

from common.cache.cache import cache_get, cache_set


class MultiLevelCache:
    """Two-level cache with local LRU memory cache backed by Redis."""

    def __init__(self, maxsize: int = 128) -> None:
        self._local: OrderedDict[str, Any] = OrderedDict()
        self._maxsize = maxsize

    def _get_local(self, key: str) -> Any | None:
        if key in self._local:
            self._local.move_to_end(key)
            return self._local[key]
        return None

    def _set_local(self, key: str, value: Any) -> None:
        self._local[key] = value
        self._local.move_to_end(key)
        if len(self._local) > self._maxsize:
            self._local.popitem(last=False)

    def _delete_local(self, key: str) -> None:
        self._local.pop(key, None)

    async def get(self, key: str) -> Any | None:
        """Try local cache, then Redis."""
        value = self._get_local(key)
        if value is not None:
            return value

        value = await cache_get(key)
        if value is not None:
            self._set_local(key, value)
        return value

    async def set(self, key: str, value: Any, ttl: int = 60) -> None:
        """Set value in both local and Redis caches."""
        self._set_local(key, value)
        await cache_set(key, value, ttl)

    async def delete(self, key: str) -> None:
        """Delete value from both caches."""
        self._delete_local(key)
        from common.cache.cache import cache_delete

        await cache_delete(key)


def multi_level_cached(
    key_prefix: str,
    ttl: int = 60,
    maxsize: int = 128,
) -> Callable:
    """Decorator for multi-level cached async function results."""
    cache = MultiLevelCache(maxsize=maxsize)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key_parts = [key_prefix]
            for arg in args[1:] if len(args) > 1 and isinstance(args[0], object) else args:
                key_parts.append(str(arg))
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}={v}")
            cache_key = ":".join(key_parts)

            value = await cache.get(cache_key)
            if value is not None:
                return json.loads(value) if isinstance(value, str) else value

            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl)
            return result

        return wrapper

    return decorator
