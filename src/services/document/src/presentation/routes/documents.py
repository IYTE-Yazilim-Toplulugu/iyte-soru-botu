from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse
from shared_kernel import ApiResponse
from typing import List, Dict, Any
import io

from src.application.commands import (
    UploadDocumentCommand,
    UploadDocumentHandler,
    DeleteDocumentCommand,
    DeleteDocumentHandler,
)
from src.application.queries import (
    GetUserDocumentsQuery,
    GetUserDocumentsHandler,
    GetDocumentQuery,
    GetDocumentHandler,
)
from src.infrastructure.data.repositories import DocumentRepository
from src.infrastructure.storage import MinIOService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = "test-user",  # TODO: Get from JWT token
) -> ApiResponse[Dict[str, str]]:
    """Upload a document."""
    try:
        # Read file data
        file_data = await file.read()
        file_stream = io.BytesIO(file_data)

        # Create handler
        repository = DocumentRepository()
        storage_service = MinIOService()
        handler = UploadDocumentHandler(repository, storage_service)

        # Create command
        command = UploadDocumentCommand(
            user_id=user_id,
            filename=file.filename or "unknown",
            file_data=file_stream,
            content_type=file.content_type or "application/octet-stream",
            file_size=len(file_data),
        )

        # Handle command
        return await handler.handle(command)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/")
async def get_user_documents(
    user_id: str = "test-user",  # TODO: Get from JWT token
) -> ApiResponse[List[Dict[str, Any]]]:
    """Get all documents for the current user."""
    try:
        repository = DocumentRepository()
        handler = GetUserDocumentsHandler(repository)

        query = GetUserDocumentsQuery(user_id=user_id)
        return await handler.handle(query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    user_id: str = "test-user",  # TODO: Get from JWT token
) -> ApiResponse[Dict[str, Any]]:
    """Get a specific document."""
    try:
        repository = DocumentRepository()
        handler = GetDocumentHandler(repository)

        query = GetDocumentQuery(document_id=document_id, user_id=user_id)
        return await handler.handle(query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    user_id: str = "test-user",  # TODO: Get from JWT token
):
    """Download a document file."""
    try:
        repository = DocumentRepository()
        storage_service = MinIOService()

        # Get document
        document = await repository.get_by_id(document_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        # Check ownership
        if document.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        # Download file
        file_data = await storage_service.download_file(
            bucket=document.file_reference.bucket,
            path=document.file_reference.path,
        )

        # Return file
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type=document.metadata.content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{document.metadata.filename}"'
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    user_id: str = "test-user",  # TODO: Get from JWT token
) -> ApiResponse[None]:
    """Delete a document."""
    try:
        repository = DocumentRepository()
        storage_service = MinIOService()
        handler = DeleteDocumentHandler(repository, storage_service)

        command = DeleteDocumentCommand(document_id=document_id, user_id=user_id)
        return await handler.handle(command)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "document"}
