from dataclasses import dataclass
from typing import Optional

from shared_kernel import Entity
from ulid import ULID

from ..enums import (
    MessageSender,
    Model,
)


@dataclass(kw_only=True)
class Message(Entity[int]):

    user_id: ULID
    chat_id: ULID
    sender: MessageSender
    content: str
    token: int
    model: Optional[Model]
    length: int

    @classmethod
    def create(
        cls,
        user_id: ULID,
        chat_id: ULID,
        sender: MessageSender,
        content: str,
        token: int,
        model: Model,
    ) -> 'Message':

        return cls(
            id=ULID(),
            user_id=user_id,
            chat_id=chat_id,
            sender=sender,
            content=content,
            token=token,
            model=model,
            length=len(content),
        )
