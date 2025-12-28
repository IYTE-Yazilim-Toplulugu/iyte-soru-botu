from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
)

TId = TypeVar('TId')  # Generic type for entity IDs


@dataclass
class Entity(ABC, Generic[TId]):
    """
    Base class for all domain entities.

    An entity has identity and lifecycle. Two entities are equal if they
    have the same ID, regardless of their other attributes.

    Attributes:
        id: Unique identifier for the entity
        created_at: Timestamp when entity was created
        updated_at: Timestamp when entity was last updated
    """

    id: TId
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @classmethod
    @abstractmethod
    def create(cls, **kwargs: Any) -> 'Entity[TId]':
        """
        Factory method to create a new entity.
        Encapsulates ID generation and initial state validation.
        """
        ...

    def __eq__(self, other: object) -> bool:
        """Entities are equal if they have the same ID."""
        if not isinstance(other, Entity):
            return False
        return bool(self.id == other.id)

    def __hash__(self) -> int:
        """Hash based on ID for use in sets and dicts."""
        return hash(self.id)
