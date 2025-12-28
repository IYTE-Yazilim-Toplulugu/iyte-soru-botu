from dataclasses import dataclass, field

from shared_kernel import DomainEvent


@dataclass
class UserCreatedEvent(DomainEvent):
    """Event raised when a new user is created."""

    user_id: str = field(default=None)
    email: str = field(default=None)
