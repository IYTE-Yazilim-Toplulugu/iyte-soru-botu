from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    List,
    TypeVar,
)

if TYPE_CHECKING:
    from .mediator import IRequest

C = TypeVar("C", bound="IRequest[Any]")  # Generic Command type


class IValidator(ABC, Generic[C]):

    @abstractmethod
    def validate(self, command: C) -> List[str]:
        """
        Validate the given data.

        Parameters:
            command (Command): The command to validate.
        Returns:
            List[str]: A list of validation error messages. Empty if valid.
        """
        ...

    def is_valid(self, command: C) -> bool:
        """
        Check if the given command is valid.
        Parameters:
            command (Command): The command to check.
        Returns:
            bool: True if valid, False otherwise.
        """
        return len(self.validate(command)) == 0
