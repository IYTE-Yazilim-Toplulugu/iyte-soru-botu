from dataclasses import dataclass, field
from datetime import datetime

from shared_kernel import DomainEvent


@dataclass
class UserPasswordChangedEvent(DomainEvent):
    """Event raised when a user's password is changed."""

    user_id: str = field(default=None)
    changed_at: datetime = field(default=None)
