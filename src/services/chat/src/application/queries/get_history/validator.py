from typing import List

from shared_kernel import IValidator

from .query import GetHistoryQuery


class GetHistoryValidator(IValidator[GetHistoryQuery]):
    def validate(self, query: GetHistoryQuery) -> List[str]:
        errors = []

        if not query.chat_id:
            errors.append("chat_id is required")

        if not query.user_id:
            errors.append("user_id is required")

        if query.limit is not None:
            if not isinstance(query.limit, int) or query.limit <= 0:
                errors.append("limit must be a positive integer if provided")

        return errors
