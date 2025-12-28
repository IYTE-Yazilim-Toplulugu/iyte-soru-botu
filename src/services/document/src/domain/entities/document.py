from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shared_kernel import AggregateRoot, DomainEvent
from ulid import ULID

from ..value_objects import DocumentMetadata, FileReference
from ..events import DocumentUploadedEvent, DocumentDeletedEvent
from ..enums import DocumentStatus, DocumentType


@dataclass
class Document(AggregateRoot[str]):
    """
    Document aggregate root.
    Represents a document uploaded by a user.
    """

    user_id: str
    metadata: DocumentMetadata
    file_reference: FileReference
    status: DocumentStatus = DocumentStatus.PENDING
    document_type: DocumentType = DocumentType.PDF
    parsed_content: Optional[str] = None
    error_message: Optional[str] = None
    domain_events: list[DomainEvent] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        user_id: str,
        filename: str,
        file_size: int,
        content_type: str,
        storage_path: str,
        **kwargs,
    ) -> "Document":
        """
        Factory method to create a new document.
        """
        document_id = str(ULID())

        # Create value objects
        metadata = DocumentMetadata(
            filename=filename,
            file_size=file_size,
            content_type=content_type,
        )

        file_reference = FileReference(
            bucket="documents",
            path=storage_path,
            url=f"/documents/{document_id}/download",
        )

        # Determine document type
        document_type = cls._determine_document_type(content_type)

        document = cls(
            id=document_id,
            user_id=user_id,
            metadata=metadata,
            file_reference=file_reference,
            document_type=document_type,
            created_at=datetime.utcnow(),
            **kwargs,
        )

        # Raise domain event
        document.add_domain_event(
            DocumentUploadedEvent(
                document_id=document_id,
                user_id=user_id,
                filename=filename,
                file_size=file_size,
            )
        )

        return document

    @staticmethod
    def _determine_document_type(content_type: str) -> DocumentType:
        """Determine document type from content type."""
        if "pdf" in content_type.lower():
            return DocumentType.PDF
        elif any(ext in content_type.lower() for ext in ["word", "docx"]):
            return DocumentType.WORD
        elif any(ext in content_type.lower() for ext in ["excel", "xlsx"]):
            return DocumentType.EXCEL
        elif any(ext in content_type.lower() for ext in ["powerpoint", "pptx"]):
            return DocumentType.POWERPOINT
        elif "text" in content_type.lower():
            return DocumentType.TEXT
        else:
            return DocumentType.OTHER

    def mark_as_processing(self) -> None:
        """Mark document as being processed."""
        self.status = DocumentStatus.PROCESSING
        self.updated_at = datetime.utcnow()

    def mark_as_completed(self, parsed_content: Optional[str] = None) -> None:
        """Mark document processing as completed."""
        self.status = DocumentStatus.COMPLETED
        self.parsed_content = parsed_content
        self.updated_at = datetime.utcnow()

    def mark_as_failed(self, error_message: str) -> None:
        """Mark document processing as failed."""
        self.status = DocumentStatus.FAILED
        self.error_message = error_message
        self.updated_at = datetime.utcnow()

    def soft_delete(self) -> None:
        """Soft delete the document."""
        self.status = DocumentStatus.DELETED
        self.updated_at = datetime.utcnow()

        self.add_domain_event(
            DocumentDeletedEvent(
                document_id=self.id,
                user_id=self.user_id,
                deleted_at=self.updated_at,
            )
        )
