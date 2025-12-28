from shared_kernel import DomainEvent
from ulid import ULID


class ChatArchiveEvent(DomainEvent):
    chat_id: ULID
