from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.infrastructure.http_client import ServiceClient
from src.middleware.rate_limit import RateLimitMiddleware

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = ServiceClient(settings.AUTH_SERVICE_URL)


@router.post("/register")
async def register(request: Request):
    """Proxy registration request to auth service."""
    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request)

    # Get request body
    body = await request.json()

    try:
        # Forward to auth service
        response = await auth_service.post("/api/v1/auth/register", json_data=body)

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service is unavailable",
        )


@router.post("/login")
async def login(request: Request):
    """Proxy login request to auth service."""
    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request)

    # Get request body
    body = await request.json()

    try:
        # Forward to auth service
        response = await auth_service.post("/api/v1/auth/login", json_data=body)

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service is unavailable",
        )


@router.get("/health")
async def auth_health():
    """Check auth service health."""
    try:
        response = await auth_service.get("/api/v1/auth/health")
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "service": "auth"},
        )
