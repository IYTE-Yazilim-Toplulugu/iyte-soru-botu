from abc import abstractmethod
from typing import Protocol

from fastapi import APIRouter


class Route(Protocol):
    """
    Protocol for defining API routes in FastAPI.
    """

    router: APIRouter

    @abstractmethod
    def setup_routes(self) -> None: ...
