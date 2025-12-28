from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from shared_kernel import Entity
from ulid import ULID


@dataclass
class UserRole(Entity[ULID]):

    user_id: ULID = field(default=None)
    role_id: int = field(default=None)

    @classmethod
    def create(cls, user_id: ULID, role_id: int, **kwargs: Any) -> 'UserRole':
        """Factory method to create a new user role."""
        return cls(
            id=ULID(),
            user_id=user_id,
            role_id=role_id,
            created_at=datetime.utcnow(),
        )
