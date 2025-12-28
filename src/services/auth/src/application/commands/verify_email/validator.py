from typing import List

from shared_kernel import IValidator

from .command import VerifyEmailCommand


class VerifyEmailValidator(IValidator[VerifyEmailCommand]):
    """Validator for verify email command."""

    def validate(self, command: VerifyEmailCommand) -> List[str]:
        """Validate verify email command."""
        errors = []

        if not command.token:
            errors.append("Verification token is required")

        return errors
