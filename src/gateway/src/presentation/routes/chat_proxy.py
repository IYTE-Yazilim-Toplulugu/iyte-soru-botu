from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials

from src.config.settings import settings
from src.infrastructure.http_client import ServiceClient
from src.middleware.auth import AuthMiddleware, security
from src.middleware.rate_limit import RateLimitMiddleware

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ServiceClient(settings.CHAT_SERVICE_URL)


@router.post("/create")
async def create_chat(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Proxy create chat request to chat service."""
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request, identifier=user["user_id"])

    # Get request body
    body = await request.json()

    try:
        # Forward to chat service with auth header
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        response = await chat_service.post(
            "/api/v1/chat/create", json_data=body, headers=headers
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is unavailable",
        )


@router.post("/send-message")
async def send_message(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Proxy send message request to chat service."""
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request, identifier=user["user_id"])

    # Get request body
    body = await request.json()

    try:
        # Forward to chat service with auth header
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        response = await chat_service.post(
            "/api/v1/chat/send-message", json_data=body, headers=headers
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is unavailable",
        )


@router.get("/")
async def get_chats(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Proxy get chats request to chat service."""
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request, identifier=user["user_id"])

    try:
        # Forward to chat service with auth header
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        response = await chat_service.get("/api/v1/chat/", headers=headers)

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is unavailable",
        )


@router.get("/{chat_id}/messages")
async def get_messages(
    chat_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Proxy get messages request to chat service."""
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request, identifier=user["user_id"])

    try:
        # Forward to chat service with auth header
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        response = await chat_service.get(
            f"/api/v1/chat/{chat_id}/messages", headers=headers
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is unavailable",
        )


@router.get("/health")
async def chat_health():
    """Check chat service health."""
    try:
        response = await chat_service.get("/api/v1/chat/health")
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "service": "chat"},
        )
