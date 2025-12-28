from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from shared_kernel import Entity
from ulid import ULID


@dataclass
class RefreshToken(Entity[ULID]):

    user_id: ULID = field(default=None)
    token_hash: str = field(default=None)
    expires_at: datetime = field(default=None)
    revoked: bool = field(default=False)

    @classmethod
    def create(cls, user_id: ULID, token_hash: str, expires_at: datetime, **kwargs: Any) -> 'RefreshToken':
        """Factory method to create a new refresh token."""
        return cls(
            id=ULID(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            revoked=False,
            created_at=datetime.utcnow(),
        )
