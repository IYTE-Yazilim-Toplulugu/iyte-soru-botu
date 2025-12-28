from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Dict,
    Generic,
    Type,
    TypeVar,
)

from pydantic import BaseModel
from sqlmodel import SQLModel

from ..entities import Entity
from ..models import ApiResponse
from .mapper import IMapper
from .repository import IRepository
from .validator import IValidator

R = TypeVar("R", bound=ApiResponse[Any])  # Generic Result type


class IRequest(ABC, Generic[R]):
    """Marker interface for Commands/Queries"""

    pass


C = TypeVar("C", bound=IRequest[Any])  # Generic Command type


class IRequestHandler(ABC, Generic[C, R]):
    """Interface for any Handler that processes a Command and returns a Result"""

    def __init__(
        self,
        repository: IRepository[Any, Entity[Any]],
        validator: IValidator[IRequest[Any]],
        mapper: IMapper[SQLModel, Entity[Any], BaseModel],
    ) -> None:
        """Initializes the handler with required dependencies."""
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    @abstractmethod
    async def handle(self, command: C) -> R:
        """Processes the command and returns a result."""
        ...


class Mediator:
    """
    The Mediator responsible for dispatching commands to the correct handler.
    """

    def __init__(self) -> None:
        # A dictionary mapping Command Types to Handler Instances
        self._registry: Dict[Type[IRequest[Any]], IRequestHandler[Any, Any]] = {}

    def register(
        self, command_type: Type[IRequest[Any]], handler: IRequestHandler[Any, Any]
    ) -> None:
        """Register a handler for a specific command type"""
        self._registry[command_type] = handler

    async def send(self, command: IRequest[Any]) -> Any:
        """Finds the handler and executes it"""
        command_type = type(command)
        handler = self._registry.get(command_type)

        if not handler:
            raise ValueError(f"No handler registered for {command_type.__name__}")

        return await handler.handle(command)
