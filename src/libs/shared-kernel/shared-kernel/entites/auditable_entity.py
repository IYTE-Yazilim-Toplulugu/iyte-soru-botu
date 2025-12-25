from dataclasses import dataclass
from typing import (
    Generic,
    Optional,
    TypeVar,
)

from .base_entity import Entity

TId = TypeVar('TId')  # Generic type for entity IDs


@dataclass
class AuditableEntity(Entity[TId], Generic[TId]):
    """
    Base class for entities that require auditing.

    Adds created_by and updated_by attributes to track who created
    and last modified the entity.
    """

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
