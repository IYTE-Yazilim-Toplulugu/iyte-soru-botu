from dataclasses import dataclass
from datetime import datetime

from shared_kernel import DomainEvent


@dataclass
class DocumentUploadedEvent(DomainEvent):
    """Event raised when a document is uploaded."""

    document_id: str
    user_id: str
    filename: str
    file_size: int
    occurred_at: datetime = datetime.utcnow()
