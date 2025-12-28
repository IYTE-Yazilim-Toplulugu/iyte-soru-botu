from dataclasses import dataclass
from typing import Dict, Any

from shared_kernel import (
    ApiResponse,
    IRequest,
    IRequestHandler,
    ResponseCode,
)

from src.domain.interfaces import IDocumentRepository
from src.domain.exceptions import (
    DocumentNotFoundException,
    DocumentAccessDeniedException,
)


@dataclass
class GetDocumentQuery(IRequest[ApiResponse[Dict[str, Any]]]):
    """Query to get a specific document."""

    document_id: str
    user_id: str


class GetDocumentHandler(
    IRequestHandler[GetDocumentQuery, ApiResponse[Dict[str, Any]]]
):
    """Handler for getting a document."""

    def __init__(self, document_repository: IDocumentRepository):
        self._document_repository = document_repository

    async def handle(self, query: GetDocumentQuery) -> ApiResponse[Dict[str, Any]]:
        """Handle get document query."""
        try:
            # Get document
            document = await self._document_repository.get_by_id(query.document_id)
            if not document:
                raise DocumentNotFoundException(query.document_id)

            # Check ownership
            if document.user_id != query.user_id:
                raise DocumentAccessDeniedException(query.document_id)

            # Convert to DTO
            document_data = {
                "id": document.id,
                "filename": document.metadata.filename,
                "file_size": document.metadata.file_size,
                "content_type": document.metadata.content_type,
                "status": document.status.value,
                "document_type": document.document_type.value,
                "download_url": document.file_reference.url,
                "parsed_content": document.parsed_content,
                "error_message": document.error_message,
                "created_at": document.created_at.isoformat(),
                "updated_at": document.updated_at.isoformat()
                if document.updated_at
                else None,
            }

            return ApiResponse[Dict[str, Any]](
                code=ResponseCode.SUCCESS,
                message="Document retrieved successfully",
                data=document_data,
            )

        except DocumentNotFoundException as e:
            return ApiResponse[Dict[str, Any]](
                code=ResponseCode.NOT_FOUND,
                message=str(e),
                data={},
            )
        except DocumentAccessDeniedException as e:
            return ApiResponse[Dict[str, Any]](
                code=ResponseCode.FORBIDDEN,
                message=str(e),
                data={},
            )
        except Exception as e:
            return ApiResponse[Dict[str, Any]](
                code=ResponseCode.INTERNAL_ERROR,
                message="Failed to retrieve document",
                data={},
            )
