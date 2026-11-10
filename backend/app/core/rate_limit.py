"""
IRONCORE Distributed Rate Limiting.
Uses Redis sliding window / counter with IP and User ID scoping.
"""
from fastapi import HTTPException, Request, status
from app.core.redis import redis_client


async def check_rate_limit(
    key_prefix: str,
    identifier: str,
    limit: int,
    window_seconds: int = 60
) -> None:
    """Enforce rate limits using Redis or fallback cache."""
    cache_key = f"ratelimit:{key_prefix}:{identifier}"
    current_count = await redis_client.incr(cache_key)
    if current_count == 1:
        await redis_client.expire(cache_key, window_seconds)

    if current_count > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Please wait before retrying.",
            headers={"Retry-After": str(window_seconds)}
        )


def get_client_ip(request: Request) -> str:
    """Extract client IP, taking into account forwarded headers behind reverse proxies."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"
