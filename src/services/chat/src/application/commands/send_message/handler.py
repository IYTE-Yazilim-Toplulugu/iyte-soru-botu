from typing import Optional

from shared_kernel import (
    ApiResponse,
    IMapper,
    IRequestHandler,
    IValidator,
)

from src.domain.entities import (
    Chat,
    Message,
)
from src.domain.enums import MessageSender
from src.domain.interfaces.chat_repository import IChatRepository
from src.domain.interfaces.llm_gateway import ILlmGateway
from src.domain.interfaces.message_repository import IMessageRepository

from ...dtos import MessageDTO
from .command import SendMessageCommand


# Use automapper in future to map entities to dtos
class SendMessageHandler(IRequestHandler[SendMessageCommand, ApiResponse[MessageDTO]]):
    def __init__(
        self,
        repository: IChatRepository,
        validator: IValidator[SendMessageCommand],
        mapper: IMapper,
        message_repository: IMessageRepository,
        llm_gateway: Optional[ILlmGateway] = None,
    ):
        super().__init__(repository, validator, mapper)
        self._message_repository = message_repository
        self._llm_gateway = llm_gateway

    async def handle(self, command: SendMessageCommand) -> MessageDTO:
        # 1. Validate command
        if not self._validator.is_valid(command):
            return ApiResponse.bad_request()

        # 2. Load chat aggregate
        chat: Chat = self._repository.find_by_id(command.chat_id)
        if chat is None:
            return ApiResponse.not_found()

        # 3. Verify user owns the chat
        if chat.user_id != command.user_id:
            return ApiResponse.forbidden()

        if chat.is_archived:
            return ApiResponse.bad_request("Cannot send message to an archived chat.")

        # 4. Create user message entity
        user_message = Message(
            chat_id=command.chat_id,
            sender=MessageSender.CLIENT,
            content=command.content,
        )

        # 6. Save user message
        self._message_repository.add(user_message)

        # 7. Update chat aggregate (increments message_count, emits domain event)
        chat.send_message(user_message)

        # 8. Persist chat aggregate changes
        self._repository.update(chat)

        # 9. Generate AI response
        if command.generate_ai_response and self._llm_gateway:
            await self._generate_ai_response(
                chat=chat,
                message=user_message,
            )

        msg_dto = self._mapper.map(user_message, MessageDTO)
        return ApiResponse.success(msg_dto)

    async def _generate_ai_response(
        self,
        chat: Chat,
        message: Message,
    ) -> Message:
        # Get conversation history
        history = self._message_repository.find_by_chat_id(chat.id, limit=20)

        # Format for LLM
        messages = [
            {
                "role": msg.sender,
                "content": msg.content,
            }
            for msg in history
        ]

        # Generate response
        ai_answer = await self._llm_gateway.generate_response(
            user_id=chat.user_id,
            messages=messages,
        )

        # Create AI message entity
        ai_message = Message(
            user_id=chat.user_id,
            chat_id=chat.id,
            sender=MessageSender.AI,
            content=ai_answer.content,
            token=ai_answer.token,
            model=ai_answer.model,
            length=len(ai_answer.content),
        )

        # Save AI message
        saved_ai_message = self._message_repository.add(ai_message)

        # Update chat aggregate again
        chat.send_message(saved_ai_message)

        self._chat_repository.add(chat)

        return saved_ai_message
