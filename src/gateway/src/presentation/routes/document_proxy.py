from fastapi import APIRouter, Request, HTTPException, status, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials

from src.config.settings import settings
from src.infrastructure.http_client import ServiceClient
from src.middleware.auth import AuthMiddleware, security
from src.middleware.rate_limit import RateLimitMiddleware

router = APIRouter(prefix="/documents", tags=["documents"])
document_service = ServiceClient(settings.DOCUMENT_SERVICE_URL)


@router.post("/upload")
async def upload_document(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Proxy document upload request to document service."""
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request, identifier=user["user_id"])

    # Get request body
    body = await request.json()

    try:
        # Forward to document service with auth header
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        response = await document_service.post(
            "/api/v1/documents/upload", json_data=body, headers=headers
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Document service is unavailable",
        )


@router.get("/")
async def get_documents(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Proxy get documents request to document service."""
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request, identifier=user["user_id"])

    try:
        # Forward to document service with auth header
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        response = await document_service.get("/api/v1/documents/", headers=headers)

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Document service is unavailable",
        )


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Proxy get document request to document service."""
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request, identifier=user["user_id"])

    try:
        # Forward to document service with auth header
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        response = await document_service.get(
            f"/api/v1/documents/{document_id}", headers=headers
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Document service is unavailable",
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Proxy delete document request to document service."""
    # Verify authentication
    user = await AuthMiddleware.get_current_user(credentials)

    # Rate limiting
    await RateLimitMiddleware.check_rate_limit(request, identifier=user["user_id"])

    try:
        # Forward to document service with auth header
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        response = await document_service.delete(
            f"/api/v1/documents/{document_id}", headers=headers
        )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Document service is unavailable",
        )


@router.get("/health")
async def document_health():
    """Check document service health."""
    try:
        response = await document_service.get("/api/v1/documents/health")
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "service": "document"},
        )
