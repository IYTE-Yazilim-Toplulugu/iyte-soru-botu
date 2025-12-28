from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Generic,
    TypeVar,
    cast,
)

from pydantic import BaseModel
from sqlmodel import SQLModel

from ..entities.base_entity import Entity

S = TypeVar('S', bound=SQLModel)  # Generic SQLModel type
D = TypeVar('D', bound=Entity[Any])  # Generic Domain Entity type
T = TypeVar('T', bound=BaseModel)  # Generic DTO type


class IMapper(ABC, Generic[S, D, T]):

    def map(
        self, source: S | D | T, target_type: type[S] | type[D] | type[T]
    ) -> S | D | T:
        """Generic mapping method to map source to target_type."""

        if isinstance(source, SQLModel) and issubclass(target_type, Entity):
            return self.to_domain(cast(S, source))

        elif isinstance(source, Entity) and issubclass(target_type, SQLModel):
            return self.to_db(source)

        elif (
            isinstance(source, Entity)
            and issubclass(target_type, BaseModel)
            and not issubclass(target_type, (SQLModel, Entity))
        ):
            return self.to_dto(source)

        elif (
            isinstance(source, BaseModel)
            and not isinstance(source, (SQLModel, Entity))
            and issubclass(target_type, Entity)
        ):
            return self.from_dto(source)

        raise ValueError(
            f"Unsupported mapping from {type(source).__name__} to {target_type.__name__}"
        )

    @abstractmethod
    def to_domain(self, db_model: S) -> D:
        """Maps a SQLModel to a Domain Entity."""
        ...

    @abstractmethod
    def to_db(self, domain_entity: D) -> S:
        """Maps a Domain Entity to a SQLModel."""
        ...

    @abstractmethod
    def to_db_update(self, domain_entity: D, db_model: S) -> S:
        """Updates a SQLModel with values from a Domain Entity."""
        ...

    @abstractmethod
    def to_dto(self, domain_entity: D) -> T:
        """Maps a Domain Entity to a Data Transfer Object (DTO)."""
        ...

    @abstractmethod
    def from_dto(self, dto: T) -> D:
        """Maps a Data Transfer Object (DTO) to a Domain Entity."""
        ...
