from abc import ABC, abstractmethod
from typing import BinaryIO, Optional


class IStorageService(ABC):
    """Interface for object storage (MinIO)."""

    @abstractmethod
    async def upload_file(
        self, bucket: str, path: str, file_data: BinaryIO, content_type: str
    ) -> str:
        """Upload a file to storage and return the URL."""
        ...

    @abstractmethod
    async def download_file(self, bucket: str, path: str) -> bytes:
        """Download a file from storage."""
        ...

    @abstractmethod
    async def delete_file(self, bucket: str, path: str) -> bool:
        """Delete a file from storage."""
        ...

    @abstractmethod
    async def get_file_url(self, bucket: str, path: str, expires_in: int = 3600) -> str:
        """Get a presigned URL for file access."""
        ...

    @abstractmethod
    async def file_exists(self, bucket: str, path: str) -> bool:
        """Check if a file exists in storage."""
        ...
