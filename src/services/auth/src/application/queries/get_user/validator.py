from typing import List

from shared_kernel import IValidator

from .query import GetUserQuery


class GetUserValidator(IValidator[GetUserQuery]):
    """Validator for get user query."""

    def validate(self, request: GetUserQuery) -> List[str]:
        """Validate get user query."""
        errors = []

        if not request.user_id:
            errors.append("User ID is required")

        return errors
