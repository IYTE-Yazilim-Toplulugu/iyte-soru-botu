from datetime import datetime
from typing import Optional

from sqlmodel import (
    Field,
    SQLModel,
)


class ChatDbModel(SQLModel, table=True):
    __tablename__ = "chats"

    # ULID format for IDs (max length 26 chars for ULID)
    id: Optional[str] = Field(default=None, primary_key=True, max_length=29)

    user_id: str = Field(foreign_key="users.id", index=True, max_length=29)

    title: Optional[str] = Field(default=None, max_length=255)
    message_count: int = Field(default=0)
    is_archived: bool = Field(default=False)

    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
                "user_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
                "title": "Financial Analysis Chat",
                "message_count": 5,
                "is_archived": False,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-02T12:00:00Z",
            }
        }
