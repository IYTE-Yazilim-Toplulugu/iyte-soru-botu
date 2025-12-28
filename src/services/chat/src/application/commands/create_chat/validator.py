from typing import List

from shared_kernel import IValidator

from .command import CreateChatCommand


class CreateChatValidator(IValidator[CreateChatCommand]):
    def validate(self, command: CreateChatCommand) -> List[str]:
        errors = []

        if not command.user_id:
            errors.append("user_id is required")

        if not command.message or not command.message.strip():
            errors.append("content is required and cannot be empty")

        if len(command.message) > 32000:
            errors.append("content exceeds maximum length of 32000 characters")

        return errors
