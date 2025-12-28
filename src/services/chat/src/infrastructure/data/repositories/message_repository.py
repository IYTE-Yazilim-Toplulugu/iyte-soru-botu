from typing import (
    List,
    Optional,
)

from sqlmodel import (
    Session,
    func,
    select,
)

from src.domain.entities import Message
from src.domain.interfaces.message_repository import IMessageRepository

from ..mappers.message_mapper import MessageMapper
from ..models.message_db_model import MessageDbModel


class MessageRepository(IMessageRepository):

    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Message) -> Message:
        raise NotImplementedError()

    def update(self, entity: Message) -> Message:
        raise NotImplementedError()

    def save(self, message: Message) -> Message:

        existing = None
        if message.id is not None:
            existing = self._session.get(MessageDbModel, message.id)

        if existing:
            db_model = MessageMapper.to_db(message)
            for key, value in db_model.dict(exclude_unset=True).items():
                setattr(existing, key, value)
            db_model = existing
        else:
            db_model = MessageMapper.to_db(message)
            self._session.add(db_model)

        self._session.commit()
        self._session.refresh(db_model)

        return MessageMapper.to_domain(db_model)

    def find_by_id(self, message_id: int) -> Optional[Message]:

        db_model = self._session.get(MessageDbModel, message_id)

        if db_model is None:
            return None

        return MessageMapper.to_domain(db_model)

    def find_by_chat_id(
        self, chat_id: str, limit: Optional[int] = None
    ) -> List[Message]:

        statement = (
            select(MessageDbModel)
            .where(MessageDbModel.chat_id == chat_id)
            .order_by(MessageDbModel.timestamp.asc())
        )

        if limit is not None:
            statement = statement.limit(limit)

        results = self._session.exec(statement).all()

        return [MessageMapper.to_domain(db_model) for db_model in results]

    def delete(self, message_id: int) -> bool:

        db_model = self._session.get(MessageDbModel, message_id)

        if db_model is None:
            return False

        self._session.delete(db_model)
        self._session.commit()

        return True

    def count_by_chat_id(self, chat_id: str) -> int:

        statement = (
            select(func.count())
            .select_from(MessageDbModel)
            .where(MessageDbModel.chat_id == chat_id)
        )

        result = self._session.exec(statement).one()
        return result

    def exists(self, message_id: int) -> bool:

        db_model = self._session.get(MessageDbModel, message_id)
        return db_model is not None
