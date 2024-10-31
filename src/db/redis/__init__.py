from typing import Optional, Any
import json
from redis.asyncio import Redis
from src.core.config import settings
from functools import lru_cache

class RedisClient:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URI, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, expire: int = None) -> None:
        """Set value in Redis"""
        if expire is None:
            expire = settings.CACHE_TTL
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def delete(self, key: str) -> None:
        """Delete key from Redis"""
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis"""
        return await self.redis.exists(key)

    async def close(self):
        """Close Redis connection"""
        await self.redis.close()

# Create Redis client instance
redis_client = RedisClient()