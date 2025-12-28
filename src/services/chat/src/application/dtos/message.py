from pydantic import BaseModel
from ulid import ULID


class MessageDTO(BaseModel):
    id: ULID
    chat_id: ULID
    sender: str
    content: str
    token: int
    model: str
    length: int
