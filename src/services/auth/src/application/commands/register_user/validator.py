from typing import List

from shared_kernel import IValidator

from .command import RegisterCommand


class RegisterValidator(IValidator[RegisterCommand]):
    """Validator for register command."""

    def validate(self, command: RegisterCommand) -> List[str]:
        """Validate register command."""
        errors = []

        if not command.email:
            errors.append("Email is required")

        if not command.password:
            errors.append("Password is required")
        elif len(command.password) < 8:
            errors.append("Password must be at least 8 characters long")

        return errors
