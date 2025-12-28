from shared_kernel import DomainEvent
from ulid import ULID


class ChatUpdateTitleEvent(DomainEvent):
    chat_id: ULID
    title: str
