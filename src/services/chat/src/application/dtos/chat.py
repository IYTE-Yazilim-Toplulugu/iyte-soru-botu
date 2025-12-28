from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from ulid import ULID


@dataclass
class ChatDTO(BaseModel):

    id: ULID
    user_id: ULID
    title: str
    message_count: int
    is_archived: bool
    updated_at: Optional[datetime] = None
