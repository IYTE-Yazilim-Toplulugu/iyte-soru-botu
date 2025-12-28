from abc import abstractmethod
from typing import Optional, List

from shared_kernel import IRepository

from ..entities import Document


class IDocumentRepository(IRepository[str, Document]):
    """Repository interface for Document aggregate."""

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Document]:
        """Find all documents for a user."""
        ...

    @abstractmethod
    async def find_by_user_and_status(
        self, user_id: str, status: str
    ) -> List[Document]:
        """Find documents by user and status."""
        ...
