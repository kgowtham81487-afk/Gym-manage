"""
IRONCORE Redis Core:
Distributed session cache & rate-limiting with graceful local fallback.
"""
import time
from typing import Optional, Dict
import redis.asyncio as aioredis
from app.core.config import settings

class InMemoryFallbackStore:
    """In-memory key-value cache used if Redis is temporarily unreachable."""
    def __init__(self):
        self._store: Dict[str, str] = {}
        self._expiry: Dict[str, float] = {}

    async def get(self, key: str) -> Optional[str]:
        now = time.time()
        if key in self._expiry and now > self._expiry[key]:
            del self._store[key]
            del self._expiry[key]
            return None
        return self._store.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        self._store[key] = value
        if ex:
            self._expiry[key] = time.time() + ex
        elif key in self._expiry:
            del self._expiry[key]
        return True

    async def incr(self, key: str) -> int:
        now = time.time()
        if key in self._expiry and now > self._expiry[key]:
            self._store[key] = "0"
            del self._expiry[key]
        val = int(self._store.get(key, "0")) + 1
        self._store[key] = str(val)
        return val

    async def expire(self, key: str, seconds: int) -> bool:
        if key in self._store:
            self._expiry[key] = time.time() + seconds
            return True
        return False

    async def delete(self, key: str) -> int:
        deleted = 0
        if key in self._store:
            del self._store[key]
            deleted = 1
        if key in self._expiry:
            del self._expiry[key]
        return deleted


class RedisClient:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self.fallback = InMemoryFallbackStore()
        self.is_connected = False

    async def connect(self):
        try:
            self.redis = aioredis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=2.0
            )
            await self.redis.ping()
            self.is_connected = True
        except Exception:
            self.is_connected = False
            self.redis = None

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str) -> Optional[str]:
        if self.is_connected and self.redis:
            try:
                return await self.redis.get(key)
            except Exception:
                pass
        return await self.fallback.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        if self.is_connected and self.redis:
            try:
                return await self.redis.set(key, value, ex=ex)
            except Exception:
                pass
        return await self.fallback.set(key, value, ex=ex)

    async def incr(self, key: str) -> int:
        if self.is_connected and self.redis:
            try:
                return await self.redis.incr(key)
            except Exception:
                pass
        return await self.fallback.incr(key)

    async def expire(self, key: str, seconds: int) -> bool:
        if self.is_connected and self.redis:
            try:
                return await self.redis.expire(key, seconds)
            except Exception:
                pass
        return await self.fallback.expire(key, seconds)

    async def delete(self, key: str) -> int:
        if self.is_connected and self.redis:
            try:
                return await self.redis.delete(key)
            except Exception:
                pass
        return await self.fallback.delete(key)


redis_client = RedisClient()
