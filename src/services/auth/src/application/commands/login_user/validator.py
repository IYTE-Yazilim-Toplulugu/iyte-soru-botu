from typing import List

from shared_kernel import IValidator

from .command import LoginCommand


class LoginValidator(IValidator[LoginCommand]):
    def validate(self, command: LoginCommand) -> List[str]:
        errors = []

        if not command.email:
            errors.append("Email is required")
        if not command.password:
            errors.append("Password is required")
        if not command.password or len(command.password) < 8:
            errors.append("Password must be at least 8 characters long")
        if not command.password or not any(char.isdigit() for char in command.password):
            errors.append("Password must contain at least one digit")

        return errors
