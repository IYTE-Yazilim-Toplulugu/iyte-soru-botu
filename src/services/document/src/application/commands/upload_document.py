from dataclasses import dataclass
from typing import BinaryIO

from shared_kernel import (
    ApiResponse,
    IRequest,
    IRequestHandler,
    ResponseCode,
)

from src.domain.entities import Document
from src.domain.interfaces import IDocumentRepository, IStorageService
from src.domain.exceptions import DocumentUploadFailedException


@dataclass
class UploadDocumentCommand(IRequest[ApiResponse[dict[str, str]]]):
    """Command to upload a document."""

    user_id: str
    filename: str
    file_data: BinaryIO
    content_type: str
    file_size: int


class UploadDocumentHandler(
    IRequestHandler[UploadDocumentCommand, ApiResponse[dict[str, str]]]
):
    """Handler for document upload."""

    def __init__(
        self,
        document_repository: IDocumentRepository,
        storage_service: IStorageService,
    ):
        self._document_repository = document_repository
        self._storage_service = storage_service

    async def handle(
        self, command: UploadDocumentCommand
    ) -> ApiResponse[dict[str, str]]:
        """Handle document upload."""
        try:
            # Generate storage path
            storage_path = f"users/{command.user_id}/{command.filename}"

            # Upload file to MinIO
            await self._storage_service.upload_file(
                bucket="documents",
                path=storage_path,
                file_data=command.file_data,
                content_type=command.content_type,
            )

            # Create document entity
            document = Document.create(
                user_id=command.user_id,
                filename=command.filename,
                file_size=command.file_size,
                content_type=command.content_type,
                storage_path=storage_path,
            )

            # Save to repository
            await self._document_repository.add(document)

            return ApiResponse[dict[str, str]](
                code=ResponseCode.SUCCESS,
                message="Document uploaded successfully",
                data={
                    "document_id": document.id,
                    "filename": command.filename,
                    "status": document.status.value,
                },
            )

        except DocumentUploadFailedException as e:
            return ApiResponse[dict[str, str]](
                code=ResponseCode.INTERNAL_ERROR,
                message=str(e),
                data=None,
            )
        except Exception as e:
            return ApiResponse[dict[str, str]](
                code=ResponseCode.INTERNAL_ERROR,
                message="Failed to upload document",
                data=None,
            )
