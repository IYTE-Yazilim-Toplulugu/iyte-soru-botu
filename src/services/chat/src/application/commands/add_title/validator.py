from typing import List

from shared_kernel import IValidator

from .command import AddTitleCommand


class AddTitleValidator(IValidator[AddTitleCommand]):

    def validate(self, command: AddTitleCommand) -> List[str]:

        errors = []

        if not command.chat_id:
            errors.append("chat_id is required")

        if not command.title or not command.title.strip():
            errors.append("title is required and cannot be empty")

        if len(command.title) > 64:
            errors.append("title exceeds maximum length of 64 characters")

        return errors
