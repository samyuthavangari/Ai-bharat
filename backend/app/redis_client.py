"""
JanSahay AI - Redis Cache Layer
Provides caching helpers with TTL-based expiry for low-bandwidth optimization.
"""

import json
import redis.asyncio as redis
from typing import Any, Optional
from app.config import get_settings

settings = get_settings()

redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get or create Redis connection."""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_client


async def cache_get(key: str) -> Optional[Any]:
    """Get value from cache."""
    try:
        r = await get_redis()
        value = await r.get(key)
        if value:
            return json.loads(value)
    except Exception:
        pass
    return None


async def cache_set(key: str, value: Any, ttl: int = None) -> bool:
    """Set value in cache with optional TTL."""
    try:
        r = await get_redis()
        ttl = ttl or settings.REDIS_TTL_SECONDS
        await r.set(key, json.dumps(value, default=str), ex=ttl)
        return True
    except Exception:
        return False


async def cache_delete(key: str) -> bool:
    """Delete a cached key."""
    try:
        r = await get_redis()
        await r.delete(key)
        return True
    except Exception:
        return False


async def cache_clear_pattern(pattern: str) -> int:
    """Clear all keys matching a pattern."""
    try:
        r = await get_redis()
        keys = []
        async for key in r.scan_iter(match=pattern):
            keys.append(key)
        if keys:
            await r.delete(*keys)
        return len(keys)
    except Exception:
        return 0


async def close_redis():
    """Close Redis connection on shutdown."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
