from fastapi import Request, HTTPException, status
from src.config.settings import settings
from src.infrastructure.cache.redis_client import redis_cache


class RateLimitMiddleware:
    """Rate limiting middleware using Redis."""

    @staticmethod
    async def check_rate_limit(request: Request, identifier: str = None) -> bool:
        """
        Check if request is within rate limit.

        Args:
            request: FastAPI request object
            identifier: Custom identifier (defaults to client IP)

        Returns:
            True if within limit

        Raises:
            HTTPException: If rate limit exceeded
        """
        # Use provided identifier or fall back to client IP
        if identifier is None:
            identifier = request.client.host if request.client else "unknown"

        # Create rate limit key
        rate_limit_key = f"rate_limit:{identifier}"

        # Get current count
        current_count = await redis_cache.get(rate_limit_key)

        if current_count is None:
            # First request in window
            await redis_cache.set(
                rate_limit_key, 1, expire_seconds=settings.RATE_LIMIT_WINDOW
            )
            return True

        # Convert to int
        current_count = int(current_count) if isinstance(current_count, str) else current_count

        if current_count >= settings.RATE_LIMIT_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW} seconds",
            )

        # Increment counter
        await redis_cache.increment(rate_limit_key)
        return True

    @staticmethod
    async def get_rate_limit_info(identifier: str) -> dict:
        """Get rate limit information for an identifier."""
        rate_limit_key = f"rate_limit:{identifier}"
        current_count = await redis_cache.get(rate_limit_key)

        if current_count is None:
            current_count = 0
        else:
            current_count = int(current_count) if isinstance(current_count, str) else current_count

        return {
            "limit": settings.RATE_LIMIT_REQUESTS,
            "window_seconds": settings.RATE_LIMIT_WINDOW,
            "current_count": current_count,
            "remaining": max(0, settings.RATE_LIMIT_REQUESTS - current_count),
        }
