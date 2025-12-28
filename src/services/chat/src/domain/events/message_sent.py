from shared_kernel import DomainEvent
from ulid import ULID


class MessageSentEvent(DomainEvent):

    chat_id: ULID
    message_id: int
    sender: str
    content: str
