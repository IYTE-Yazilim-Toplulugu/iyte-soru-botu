from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Iterator,
    cast,
)


@dataclass(frozen=True)
class ValueObject(ABC):
    """
    Base class for value objects.

    Value objects are immutable and have no identity. Two value objects
    are equal if all their attributes are equal.

    Subclasses must implement get_equality_components() to define which
    components are used for equality comparison.
    """

    @abstractmethod
    def get_equality_components(self) -> Iterator[object]:
        """
        Return the components that define equality for this value object.

        Returns:
            Iterator of objects that will be used for equality comparison.
        """
        ...

    def __eq__(self, obj: object) -> bool:
        """
        Compare two value objects based on their equality components.

        Args:
            other: The object to compare with.

        Returns:
            True if objects are equal, False otherwise.
        """
        if obj is None or type(obj) is not type(self):
            return False

        other = cast(ValueObject, obj)
        return all(
            a == b
            for a, b in zip(
                self.get_equality_components(), other.get_equality_components()
            )
        )

    def __hash__(self) -> int:
        """
        Generate hash code based on equality components.

        Returns:
            Hash code for this value object.
        """
        return hash(tuple(self.get_equality_components()))

    def __ne__(self, other: object) -> bool:
        """
        Check inequality between two value objects.

        Args:
            other: The object to compare with.

        Returns:
            True if objects are not equal, False otherwise.
        """
        return not self.__eq__(other)
