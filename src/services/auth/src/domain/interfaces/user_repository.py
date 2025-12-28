from abc import abstractmethod
from typing import Optional

from shared_kernel import IRepository

from ..entities import User


class IUserRepository(IRepository[str, User]):
    """Repository interface for User aggregate."""

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email address."""
        ...

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        ...

    @abstractmethod
    async def find_by_reset_token(self, token: str) -> Optional[User]:
        """Find a user by reset token."""
        ...

    @abstractmethod
    async def find_by_verification_token(self, token: str) -> Optional[User]:
        """Find a user by verification token."""
        ...
