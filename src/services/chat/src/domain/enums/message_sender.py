from enum import StrEnum
from typing import List


class MessageSender(StrEnum):
    AI = "ai"
    CLIENT = "client"

    @property
    def values() -> List[str]:
        return [sender.value for sender in MessageSender]
