from shared_kernel import (
    ApiResponse,
    IRequestHandler,
)

from src.domain.entities import Chat

from ...dtos import ChatDTO
from .command import CreateChatCommand


class CreateChatHandler(IRequestHandler[CreateChatCommand, ApiResponse[ChatDTO]]):
    async def handle(self, command: CreateChatCommand) -> ApiResponse[ChatDTO]:
        validator = self._validator()
        if not validator.is_valid(command):
            return ApiResponse.bad_request()

        chat = Chat.create(user_id=command.user_id)

        self._repository.add(chat)

        return ApiResponse.success(self._mapper.map(chat, ChatDTO))
