from fastapi import Depends
from shared_kernel import Mediator
from sqlmodel import Session

from src.infrastructure.data.database import get_session
from src.infrastructure.data.mappers import ChatMapper
from src.infrastructure.data.repositories import (
    ChatRepository,
    MessageRepository,
)

from .commands.add_title import (
    AddTitleCommand,
    AddTitleHandler,
    AddTitleValidator,
)
from .commands.create_chat import (
    CreateChatCommand,
    CreateChatHandler,
    CreateChatValidator,
)
from .queries.get_history import (
    GetHistoryHandler,
    GetHistoryQuery,
    GetHistoryValidator,
)


def get_mediator(session: Session = Depends(get_session)) -> Mediator:

    mediator = Mediator()

    # 1. Create Dependencies
    chat_repo = ChatRepository(session)  # Or get from DB session
    message_repo = MessageRepository(session)  # Replace with actual MessageRepository

    # 2. Create Handlers with Dependencies
    create_chat_handler = CreateChatHandler(
        chat_repo, CreateChatValidator(), ChatMapper()
    )
    add_title_handler = AddTitleHandler(chat_repo, AddTitleValidator(), ChatMapper())
    get_history_handler = GetHistoryHandler(
        chat_repo,
        GetHistoryValidator(),
        ChatMapper(),
        message_repo,
    )
    # get_chat_handler = GetChatHandler(repository=chat_repo)
    # get_all_chats_handler = GetAllChatsHandler(repository=chat_repo)

    # 3. Register Handlers to Mediator
    mediator.register(CreateChatCommand, create_chat_handler)
    mediator.register(AddTitleCommand, add_title_handler)
    mediator.register(GetHistoryQuery, get_history_handler)
    # mediator.register(GetChatQuery, get_chat_handler)
    # mediator.register(GetAllChatsQuery, get_all_chats_handler)

    return mediator
