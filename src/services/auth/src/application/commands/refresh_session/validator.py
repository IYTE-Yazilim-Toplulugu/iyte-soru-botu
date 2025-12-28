from typing import List

from shared_kernel import IValidator

from .command import RefreshSessionCommand


class RefreshSessionValidator(IValidator[RefreshSessionCommand]):
    """Validator for refresh session command."""

    def validate(self, command: RefreshSessionCommand) -> List[str]:
        """Validate refresh session command."""
        errors = []

        if not command.refresh_token:
            errors.append("Refresh token is required")

        return errors
