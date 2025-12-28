from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    List,
    TypeVar,
)

from ..events.domain_event import DomainEvent
from .base_entity import Entity

TId = TypeVar('TId')  # Generic type for entity IDs


@dataclass
class AggregateRoot(Entity[TId], Generic[TId]):
    """
    Base class for aggregate roots in Domain-Driven Design.

    An aggregate root is the entry point for all operations on an aggregate.
    It maintains consistency boundaries and can emit domain events.

    Domain events are collected during business operations and can be
    dispatched by the infrastructure layer after persistence.
    """

    _domain_events: List[DomainEvent] = field(
        default_factory=list, init=False, repr=False
    )

    def add_domain_event(self, event: DomainEvent) -> None:
        """Add a domain event to be dispatched after persistence."""
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Clear all collected domain events."""
        self._domain_events.clear()

    def get_domain_events(self) -> List[DomainEvent]:
        """Get all collected domain events."""
        return self._domain_events.copy()
