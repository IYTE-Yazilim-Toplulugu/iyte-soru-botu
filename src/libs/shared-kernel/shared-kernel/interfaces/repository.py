from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
)

from ..entities import Entity

TId = TypeVar('TId')  # Generic type for entity IDs
E = TypeVar('E', bound=Entity[Any])  # Generic type for entities


class IRepository(ABC, Generic[TId, E]):

    @abstractmethod
    async def find_by_id(self, entity_id: TId) -> Optional[E]:
        """
        Finds an entity by its ID.

        Parameters:
            entity_id: The ID of the entity to find.
        """
        ...

    @abstractmethod
    async def add(self, entity: E) -> None:
        """
        Adds a new entity to the repository.

        Parameters:
            entity: The entity to be added.
        """
        ...

    @abstractmethod
    async def update(self, entity: E) -> None:
        """
        Updates an existing entity in the repository.

        Parameters:
            entity: The entity with updated data.
        """

        ...

    @abstractmethod
    async def delete(self, entity_id: TId) -> None:
        """
        Deletes an entity by its ID.

        Parameters:
            entity_id: The ID of
        """
        ...

    @abstractmethod
    async def exists(self, entity_id: TId) -> bool:
        """
        Checks if an entity exists by its ID.

        Parameters:
            entity_id: The ID of the entity to check.

        Returns:
            bool: True if the entity exists, False otherwise.
        """
        ...
