from dataclasses import dataclass
from typing import List, Dict, Any

from shared_kernel import (
    ApiResponse,
    IRequest,
    IRequestHandler,
    ResponseCode,
)

from src.domain.interfaces import IDocumentRepository


@dataclass
class GetUserDocumentsQuery(IRequest[ApiResponse[List[Dict[str, Any]]]]):
    """Query to get all documents for a user."""

    user_id: str


class GetUserDocumentsHandler(
    IRequestHandler[GetUserDocumentsQuery, ApiResponse[List[Dict[str, Any]]]]
):
    """Handler for getting user documents."""

    def __init__(self, document_repository: IDocumentRepository):
        self._document_repository = document_repository

    async def handle(
        self, query: GetUserDocumentsQuery
    ) -> ApiResponse[List[Dict[str, Any]]]:
        """Handle get user documents query."""
        try:
            # Get documents for user
            documents = await self._document_repository.find_by_user_id(query.user_id)

            # Convert to DTOs
            document_list = [
                {
                    "id": doc.id,
                    "filename": doc.metadata.filename,
                    "file_size": doc.metadata.file_size,
                    "content_type": doc.metadata.content_type,
                    "status": doc.status.value,
                    "document_type": doc.document_type.value,
                    "created_at": doc.created_at.isoformat(),
                    "updated_at": doc.updated_at.isoformat()
                    if doc.updated_at
                    else None,
                }
                for doc in documents
                if doc.status.value != "deleted"  # Exclude deleted documents
            ]

            return ApiResponse[List[Dict[str, Any]]](
                code=ResponseCode.SUCCESS,
                message=f"Found {len(document_list)} documents",
                data=document_list,
            )

        except Exception as e:
            return ApiResponse[List[Dict[str, Any]]](
                code=ResponseCode.INTERNAL_ERROR,
                message="Failed to retrieve documents",
                data=[],
            )
