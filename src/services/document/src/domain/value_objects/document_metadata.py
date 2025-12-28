from dataclasses import dataclass

from shared_kernel import ValueObject, DomainException


@dataclass(frozen=True)
class DocumentMetadata(ValueObject):
    """Document metadata value object."""

    filename: str
    file_size: int
    content_type: str

    def __post_init__(self):
        """Validate metadata."""
        if not self.filename:
            raise DomainException("Filename cannot be empty")

        if self.file_size <= 0:
            raise DomainException("File size must be positive")

        if self.file_size > 100 * 1024 * 1024:  # 100 MB
            raise DomainException("File size exceeds maximum allowed (100 MB)")

        if not self.content_type:
            raise DomainException("Content type cannot be empty")
