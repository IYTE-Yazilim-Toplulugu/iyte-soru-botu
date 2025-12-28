from typing import List

from shared_kernel import IValidator

from .command import ResetPasswordCommand


class ResetPasswordValidator(IValidator[ResetPasswordCommand]):
    """Validator for reset password command."""

    def validate(self, command: ResetPasswordCommand) -> List[str]:
        """Validate reset password command."""
        errors = []

        if not command.token:
            errors.append("Reset token is required")

        if not command.new_password:
            errors.append("New password is required")
        elif len(command.new_password) < 8:
            errors.append("Password must be at least 8 characters long")

        return errors
