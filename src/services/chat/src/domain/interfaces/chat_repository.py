from abc import abstractmethod
from typing import List

from shared_kernel import IRepository
from ulid import ULID

from ..entities.chat import Chat


class IChatRepository(IRepository[ULID, Chat]):
    @abstractmethod
    def find_by_user_id(
        self, user_id: str, include_archived: bool = False
    ) -> List[Chat]:
        """
        Find all chat sessions for a user.

        Args:
            user_id: The user ID to search for
            include_archived: Whether to include archived chats

        Returns:
            List of chat sessions (may be empty)
        """
        ...
