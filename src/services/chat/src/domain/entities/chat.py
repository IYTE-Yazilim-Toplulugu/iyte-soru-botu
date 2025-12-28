from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shared_kernel import AggregateRoot
from ulid import ULID

from ..events import (
    ChatArchiveEvent,
    ChatUpdateTitleEvent,
    MessageSentEvent,
)
from .message import Message


@dataclass(kw_only=True)
class Chat(AggregateRoot[ULID]):
    user_id: ULID
    title: Optional[str] = None
    message_count: int = 0
    is_archived: bool = False

    @classmethod
    def create(cls, user_id: ULID) -> "Chat":
        return cls(
            id=ULID(),
            user_id=user_id,
        )

    def send_message(self, message: Message) -> None:
        self.message_count += 1
        self.updated_at = datetime.utcnow()

        # Emit domain event for side effects (notifications, analytics, etc.)
        event = MessageSentEvent(
            chat_id=self.id,
            message_id=message.id,
            sender=message.sender,
            content=message.content,
        )
        self.add_domain_event(event)

    def archive(self) -> None:
        if not self.is_archived:
            self.is_archived = True
            self.updated_at = datetime.utcnow()

        event = ChatArchiveEvent(
            chat_id=self.id,
        )
        self.add_domain_event(event)

    def unarchive(self) -> None:
        if self.is_archived:
            self.is_archived = False
            self.updated_at = datetime.utcnow()

    def update_title(self, new_title: str) -> None:
        self.title = new_title.strip()
        self.updated_at = datetime.utcnow()

        event = ChatUpdateTitleEvent(
            chat_id=self.id,
            title=new_title,
        )
        self.add_domain_event(event)
