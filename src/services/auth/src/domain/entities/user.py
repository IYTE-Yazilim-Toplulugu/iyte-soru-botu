from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shared_kernel import AggregateRoot
from ulid import ULID

from ..events import (
    UserCreatedEvent,
    UserPasswordChangedEvent,
)
from ..value_objects import (
    Email,
    HashedPassword,
)


@dataclass
class User(AggregateRoot[ULID]):
    """
    User aggregate root.
    Represents a user in the authentication system.
    """

    email: Email = field(default=None)
    password_hash: HashedPassword = field(default=None)
    first_name: Optional[str] = field(default=None)
    last_name: Optional[str] = field(default=None)
    is_active: bool = field(default=True)
    email_verified: bool = field(default=False)
    verification_token: Optional[str] = field(default=None)
    reset_token: Optional[str] = field(default=None)
    last_login: Optional[datetime] = field(default=None)

    @classmethod
    def create(
        cls,
        email: str,
        password: str,
        **kwargs,
    ) -> "User":
        """
        Factory method to create a new user.
        """
        user_id = ULID()
        email = Email(email)
        hashed_password = HashedPassword.from_plain(password)

        user = cls(
            id=user_id,
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            **kwargs,
        )

        user.add_domain_event(
            UserCreatedEvent(
                user_id=user_id,
                email=str(email),
            )
        )

        return user

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the user's password."""
        return self.hashed_password.verify(password)

    def change_password(self, new_password: str) -> None:
        """Change the user's password."""
        self.hashed_password = HashedPassword.from_plain(new_password)
        self.updated_at = datetime.utcnow()

        self.add_domain_event(
            UserPasswordChangedEvent(
                user_id=self.id,
                changed_at=self.updated_at,
            )
        )

    def verify_email(self) -> None:
        """Mark the user's email as verified."""
        self.is_verified = True
        self.verification_token = None
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
