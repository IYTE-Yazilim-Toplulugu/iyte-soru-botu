from fastapi import APIRouter
from src.config.settings import settings
from src.infrastructure.cache.redis_client import redis_cache

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Gateway health check endpoint."""
    # Check Redis connectivity
    redis_status = "healthy"
    try:
        await redis_cache.set("health_check", "ok", expire_seconds=10)
        result = await redis_cache.get("health_check")
        if result != "ok":
            redis_status = "unhealthy"
    except Exception:
        redis_status = "unhealthy"

    return {
        "service": "gateway",
        "status": "healthy" if redis_status == "healthy" else "degraded",
        "version": settings.API_VERSION,
        "components": {
            "redis": redis_status,
        },
    }


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.API_VERSION,
        "status": "running",
        "endpoints": {
            "auth": f"/api/{settings.API_VERSION}/auth",
            "chat": f"/api/{settings.API_VERSION}/chat",
            "documents": f"/api/{settings.API_VERSION}/documents",
            "health": "/health",
        },
    }
