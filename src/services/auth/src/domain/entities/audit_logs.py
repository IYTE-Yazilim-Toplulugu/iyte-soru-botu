from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

from shared_kernel import Entity
from ulid import ULID

from ..enums import (
    Action,
    UserAgent,
)
from ..value_objects import Ip


@dataclass
class AuditLogs(Entity[ULID]):

    user_id: ULID = field(default=None)
    action: Action = field(default=None)
    ip_address: Ip = field(default=None)
    user_agent: UserAgent = field(default=None)
    metadata: Dict[str, str] = field(default=None)

    @classmethod
    def create(
        cls,
        user_id: ULID,
        action: Action,
        ip_address: Ip,
        user_agent: UserAgent,
        metadata: Dict,
    ) -> 'AuditLogs':

        return cls(
            id=ULID(),
            user_id=user_id,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata,
            created_at=datetime.utcnow(),
        )
