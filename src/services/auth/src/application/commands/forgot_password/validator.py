from typing import List

from shared_kernel import IValidator

from .command import ForgotPasswordCommand


class ForgotPasswordValidator(IValidator[ForgotPasswordCommand]):
    """Validator for forgot password command."""

    def validate(self, command: ForgotPasswordCommand) -> List[str]:
        """Validate forgot password command."""
        errors = []

        if not command.email:
            errors.append("Email is required")

        return errors
