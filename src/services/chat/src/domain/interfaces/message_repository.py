from abc import abstractmethod
from typing import (
    List,
    Optional,
)

from shared_kernel import IRepository

from src.domain.entities import Message


class IMessageRepository(IRepository[int, Message]):

    @abstractmethod
    def find_by_chat_id(
        self, chat_id: str, limit: Optional[int] = None
    ) -> List[Message]:
        """
        Find all messages for a chat session.

        Args:
            chat_id: The chat ID to search for
            limit: Optional limit on number of messages to return

        Returns:
            List of messages ordered by timestamp (may be empty)
        """
        ...

    @abstractmethod
    def count_by_chat_id(self, chat_id: str) -> int:
        """
        Count messages in a chat session.

        Args:
            chat_id: The chat ID

        Returns:
            Number of messages
        """
        ...
