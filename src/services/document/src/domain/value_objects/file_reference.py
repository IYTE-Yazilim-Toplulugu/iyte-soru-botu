from dataclasses import dataclass

from shared_kernel import ValueObject


@dataclass(frozen=True)
class FileReference(ValueObject):
    """File reference value object for MinIO storage."""

    bucket: str
    path: str
    url: str

    def get_full_path(self) -> str:
        """Get full storage path."""
        return f"{self.bucket}/{self.path}"
