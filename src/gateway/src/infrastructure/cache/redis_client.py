import json
from typing import Optional, Any
import redis.asyncio as aioredis
from src.config.settings import settings


class RedisCache:
    """Redis cache client for session management."""

    def __init__(self):
        self._redis: Optional[aioredis.Redis] = None

    async def connect(self):
        """Connect to Redis."""
        self._redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            encoding="utf-8",
            decode_responses=True,
        )

    async def disconnect(self):
        """Disconnect from Redis."""
        if self._redis:
            await self._redis.close()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self._redis:
            return None
        value = await self._redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def set(
        self, key: str, value: Any, expire_seconds: Optional[int] = None
    ) -> bool:
        """Set value in cache with optional expiration."""
        if not self._redis:
            return False

        if expire_seconds is None:
            expire_seconds = settings.SESSION_EXPIRE_SECONDS

        # Serialize to JSON if not a string
        if not isinstance(value, str):
            value = json.dumps(value)

        await self._redis.set(key, value, ex=expire_seconds)
        return True

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self._redis:
            return False
        await self._redis.delete(key)
        return True

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self._redis:
            return False
        return bool(await self._redis.exists(key))

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter."""
        if not self._redis:
            return 0
        return await self._redis.incrby(key, amount)

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration on a key."""
        if not self._redis:
            return False
        return await self._redis.expire(key, seconds)


# Global instance
redis_cache = RedisCache()
