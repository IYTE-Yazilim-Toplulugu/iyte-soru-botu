from dataclasses import dataclass
from datetime import datetime

from shared_kernel import DomainEvent


@dataclass
class DocumentDeletedEvent(DomainEvent):
    """Event raised when a document is deleted."""

    document_id: str
    user_id: str
    deleted_at: datetime
    occurred_at: datetime = datetime.utcnow()
