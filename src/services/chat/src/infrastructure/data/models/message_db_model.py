from typing import Optional

from sqlmodel import (
    Field,
    SQLModel,
)

from src.domain.enums import (
    MessageSender,
    Model,
)


class MessageDbModel(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: str = Field(foreign_key="users.id", index=True, max_length=29)
    chat_id: str = Field(foreign_key="chats.id", index=True, max_length=29)

    # embedding_id: Optional[str] = Field(
    #     foreign_key="embeddings.id", default=None, index=True
    # )

    sender: MessageSender
    content: str
    token: int
    model: Optional[Model] = Field(default=None)
    length: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
                "chat_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
                "sender": "user",
                "content": "What's my account balance?",
                "token": 7,
                "model": Model.GEMINI,
                "length": 28,
            }
        }
