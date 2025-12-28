from typing import BinaryIO
from minio import Minio
from minio.error import S3Error
import io

from src.domain.interfaces import IStorageService
from src.domain.exceptions import StorageException
from src.infrastructure.config.settings import settings


class MinIOService(IStorageService):
    """MinIO storage service implementation."""

    def __init__(self):
        self._client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the bucket exists."""
        try:
            if not self._client.bucket_exists(settings.MINIO_BUCKET):
                self._client.make_bucket(settings.MINIO_BUCKET)
        except S3Error as e:
            raise StorageException(f"Failed to create bucket: {str(e)}")

    async def upload_file(
        self, bucket: str, path: str, file_data: BinaryIO, content_type: str
    ) -> str:
        """Upload a file to MinIO."""
        try:
            # Get file size
            file_data.seek(0, 2)  # Seek to end
            file_size = file_data.tell()
            file_data.seek(0)  # Seek back to start

            # Upload file
            self._client.put_object(
                bucket,
                path,
                file_data,
                file_size,
                content_type=content_type,
            )

            return f"/{bucket}/{path}"

        except S3Error as e:
            raise StorageException(f"Failed to upload file: {str(e)}")

    async def download_file(self, bucket: str, path: str) -> bytes:
        """Download a file from MinIO."""
        try:
            response = self._client.get_object(bucket, path)
            data = response.read()
            response.close()
            response.release_conn()
            return data

        except S3Error as e:
            raise StorageException(f"Failed to download file: {str(e)}")

    async def delete_file(self, bucket: str, path: str) -> bool:
        """Delete a file from MinIO."""
        try:
            self._client.remove_object(bucket, path)
            return True

        except S3Error as e:
            raise StorageException(f"Failed to delete file: {str(e)}")

    async def get_file_url(self, bucket: str, path: str, expires_in: int = 3600) -> str:
        """Get a presigned URL for file access."""
        try:
            from datetime import timedelta

            url = self._client.presigned_get_object(
                bucket, path, expires=timedelta(seconds=expires_in)
            )
            return url

        except S3Error as e:
            raise StorageException(f"Failed to generate URL: {str(e)}")

    async def file_exists(self, bucket: str, path: str) -> bool:
        """Check if a file exists in MinIO."""
        try:
            self._client.stat_object(bucket, path)
            return True
        except S3Error:
            return False
