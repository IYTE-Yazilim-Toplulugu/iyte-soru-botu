from typing import (
    List,
    Optional,
)

from sqlmodel import (
    Session,
    select,
)

from src.domain.entities.chat import Chat
from src.domain.interfaces.chat_repository import IChatRepository

from ..mappers.chat_mapper import ChatMapper
from ..models.chat_db_model import ChatDbModel


class ChatRepository(IChatRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, enlity: Chat) -> Chat:
        raise NotImplementedError()

    def update(self, entity: Chat) -> Chat:
        raise NotImplementedError()

    def save(self, chat: Chat) -> Chat:
        existing = self._session.get(ChatDbModel, chat.id)

        if existing:
            db_model = ChatMapper.to_db_update(chat, existing)
        else:
            db_model = ChatMapper.to_db(chat)
            self._session.add(db_model)

        self._session.commit()
        self._session.refresh(db_model)

        # Clear domain events after successful persistence
        # (In real system, dispatch events before clearing)
        chat.clear_domain_events()

        return ChatMapper.to_domain(db_model)

    def find_by_id(self, chat_id: str) -> Optional[Chat]:
        db_model = self._session.get(ChatDbModel, chat_id)

        if db_model is None:
            return None

        return ChatMapper.to_domain(db_model)

    def find_by_user_id(
        self, user_id: str, include_archived: bool = False
    ) -> List[Chat]:
        statement = select(ChatDbModel).where(ChatDbModel.user_id == user_id)

        if not include_archived:
            statement = statement.where(ChatDbModel.is_archived is False)

        statement = statement.order_by(ChatDbModel.updated_at.desc())

        results = self._session.exec(statement).all()

        return [ChatMapper.to_domain(db_model) for db_model in results]

    def delete(self, chat_id: str) -> bool:
        db_model = self._session.get(ChatDbModel, chat_id)

        if db_model is None:
            return False

        self._session.delete(db_model)
        self._session.commit()

        return True

    def exists(self, chat_id: str) -> bool:
        db_model = self._session.get(ChatDbModel, chat_id)
        return db_model is not None
