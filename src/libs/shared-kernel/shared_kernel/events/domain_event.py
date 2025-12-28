from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime


@dataclass
class DomainEvent(ABC):
    """
    Base class for domain events.

    Domain events represent something that happened in the domain that
    domain experts care about.

    Attributes:
        occurred_at: Timestamp when the event occurred
    """

    occurred_at: datetime = field(default_factory=datetime.utcnow)
