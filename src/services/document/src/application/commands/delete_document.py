from dataclasses import dataclass

from shared_kernel import (
    ApiResponse,
    IRequest,
    IRequestHandler,
    ResponseCode,
)

from src.domain.interfaces import IDocumentRepository, IStorageService
from src.domain.exceptions import (
    DocumentNotFoundException,
    DocumentAccessDeniedException,
)


@dataclass
class DeleteDocumentCommand(IRequest[ApiResponse[None]]):
    """Command to delete a document."""

    document_id: str
    user_id: str


class DeleteDocumentHandler(IRequestHandler[DeleteDocumentCommand, ApiResponse[None]]):
    """Handler for document deletion."""

    def __init__(
        self,
        document_repository: IDocumentRepository,
        storage_service: IStorageService,
    ):
        self._document_repository = document_repository
        self._storage_service = storage_service

    async def handle(self, command: DeleteDocumentCommand) -> ApiResponse[None]:
        """Handle document deletion."""
        try:
            # Get document
            document = await self._document_repository.get_by_id(command.document_id)
            if not document:
                raise DocumentNotFoundException(command.document_id)

            # Check ownership
            if document.user_id != command.user_id:
                raise DocumentAccessDeniedException(command.document_id)

            # Soft delete document
            document.soft_delete()
            await self._document_repository.update(document)

            # Delete from storage
            await self._storage_service.delete_file(
                bucket=document.file_reference.bucket,
                path=document.file_reference.path,
            )

            return ApiResponse[None](
                code=ResponseCode.SUCCESS,
                message="Document deleted successfully",
                data=None,
            )

        except DocumentNotFoundException as e:
            return ApiResponse[None](
                code=ResponseCode.NOT_FOUND,
                message=str(e),
                data=None,
            )
        except DocumentAccessDeniedException as e:
            return ApiResponse[None](
                code=ResponseCode.FORBIDDEN,
                message=str(e),
                data=None,
            )
        except Exception as e:
            return ApiResponse[None](
                code=ResponseCode.INTERNAL_ERROR,
                message="Failed to delete document",
                data=None,
            )
