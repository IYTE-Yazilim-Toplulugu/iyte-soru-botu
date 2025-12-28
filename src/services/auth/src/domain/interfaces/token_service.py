from abc import ABC, abstractmethod
from typing import Dict, Any


class ITokenService(ABC):
    """Interface for JWT token generation and validation."""

    @abstractmethod
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create a new access token."""
        ...

    @abstractmethod
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create a new refresh token."""
        ...

    @abstractmethod
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a token."""
        ...
