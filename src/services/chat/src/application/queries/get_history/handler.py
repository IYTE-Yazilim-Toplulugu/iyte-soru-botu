from typing import List

from shared_kernel import (
    ApiResponse,
    IMapper,
    IRequestHandler,
    IValidator,
)

from src.domain.interfaces.chat_repository import IChatRepository
from src.domain.interfaces.message_repository import IMessageRepository

from ...dtos import MessageDTO
from .query import GetHistoryQuery
from .validator import GetHistoryValidator


class GetHistoryHandler(
    IRequestHandler[GetHistoryQuery, ApiResponse[List[MessageDTO]]]
):
    def __init__(
        self,
        chat_repository: IChatRepository,
        validator: IValidator[GetHistoryQuery],
        mapper: IMapper,
        message_repository: IMessageRepository,
    ) -> None:
        super().__init__(chat_repository, validator, mapper)
        self._message_repository = message_repository

    def handle(self, query: GetHistoryQuery) -> ApiResponse[List[MessageDTO]]:
        if not GetHistoryValidator.is_valid(query):
            return ApiResponse.bad_request()

        chat = self._chat_repository.find_by_id(query.chat_id)

        if chat is None:
            return ApiResponse.not_found()

        if chat.user_id != query.user_id:
            return ApiResponse.forbidden()

        messages = self._message_repository.find_by_chat_id(
            chat_id=query.chat_id,
            limit=query.limit,
        )

        return ApiResponse.success(self._mapper.map_list(messages, MessageDTO))
