import re
from dataclasses import dataclass

from shared_kernel import ValueObject, DomainException


@dataclass(frozen=True)
class Email(ValueObject):
    """Email value object with validation."""

    value: str

    def __post_init__(self):
        """Validate email format."""
        if not self._is_valid_email(self.value):
            raise DomainException(f"Invalid email format: {self.value}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Simple email validation."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        return self.value
