import bcrypt
from dataclasses import dataclass

from shared_kernel import ValueObject


@dataclass(frozen=True)
class HashedPassword(ValueObject):
    """Hashed password value object."""

    value: str

    @classmethod
    def from_plain(cls, plain_password: str) -> "HashedPassword":
        """Create a HashedPassword from a plain text password."""
        if len(plain_password) < 8:
            from shared_kernel import DomainException

            raise DomainException("Password must be at least 8 characters long")

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return cls(value=hashed.decode("utf-8"))

    def verify(self, plain_password: str) -> bool:
        """Verify a plain text password against this hash."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self.value.encode("utf-8")
        )
