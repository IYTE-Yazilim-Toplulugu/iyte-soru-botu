from shared_kernel import (
    ApiResponse,
    IRequestHandler,
)

from src.domain.entities import Chat

from .command import AddTitleCommand


class AddTitleHandler(IRequestHandler[AddTitleCommand, ApiResponse[None]]):

    async def handle(self, command: AddTitleCommand) -> ApiResponse[None]:

        validator = self._validator()
        if not validator.is_valid(command):
            return ApiResponse.bad_request()

        chat: Chat = await self._repository.get_by_id(command.chat_id)

        if chat.user_id != command.user_id:
            return ApiResponse.forbidden()

        chat.update_title(command.title)

        self._repository.update(chat)

        return chat
