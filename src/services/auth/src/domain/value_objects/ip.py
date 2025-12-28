from dataclasses import dataclass
from typing import Iterator

from shared_kernel import ValueObject


@dataclass(frozen=True)
class Ip(ValueObject):
    """IP address value object."""

    value: str

    def __post_init__(self):
        """Validate IP address format."""
        octets = self.value.split('.')
        if len(octets) != 4 or not all(
            o.isdigit() and 0 <= int(o) <= 255 for o in octets
        ):
            raise ValueError(f"Invalid IP address: {self.value}")

    def get_equality_components(self) -> Iterator[object]:
        """Return components for equality comparison."""
        yield self.value
