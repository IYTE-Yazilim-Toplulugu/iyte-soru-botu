from typing import List

from shared_kernel import IValidator

from .command import SendMessageCommand


class SendMessageValidator(IValidator[SendMessageCommand]):
    def validate(command: SendMessageCommand) -> List[str]:
        errors = []

        if not command.chat_id:
            errors.append("chat_id is required")

        if not command.user_id:
            errors.append("user_id is required")

        if not command.content or not command.content.strip():
            errors.append("content is required and cannot be empty")

        if len(command.content) > 32000:
            errors.append("content exceeds maximum length of 32000 characters")

        if command.model and not command.model.strip():
            errors.append("model cannot be empty if provided")

        return errors
