from shared_kernel.interfaces.mapper import IMapper

from src.application.dtos import MessageDTO
from src.domain.entities import Message

from ..models.message_db_model import MessageDbModel


class MessageMapper(IMapper[MessageDbModel, Message, MessageDTO]):

    def to_domain(self, db_model: MessageDbModel) -> Message:

        return Message(
            id=db_model.id,
            chat_id=db_model.chat_id,
            sender=db_model.sender,
            content=db_model.content,
            token=db_model.token,
            model=db_model.model,
            length=db_model.length,
        )

    def to_db(self, domain_entity: Message) -> MessageDbModel:

        return MessageDbModel(
            id=domain_entity.id,
            chat_id=domain_entity.chat_id,
            sender=domain_entity.sender,
            content=domain_entity.content,
            token=domain_entity.token,
            model=domain_entity.model,
            length=domain_entity.length,
        )

    def to_db_update(
        self, domain_entity: Message, db_model: MessageDbModel
    ) -> MessageDbModel:

        db_model.chat_id = domain_entity.chat_id
        db_model.sender = domain_entity.sender
        db_model.content = domain_entity.content
        db_model.token = domain_entity.token
        db_model.model = domain_entity.model
        db_model.length = domain_entity.length

        return db_model

    def to_dto(self, domain_entity: Message) -> MessageDTO:

        return MessageDTO(
            id=domain_entity.id,
            chat_id=domain_entity.chat_id,
            sender=domain_entity.sender,
            content=domain_entity.content,
            token=domain_entity.token,
            model=domain_entity.model,
            length=domain_entity.length,
        )

    def from_dto(self, dto: MessageDTO) -> Message:

        return Message(
            id=dto.id,
            chat_id=dto.chat_id,
            sender=dto.sender,
            content=dto.content,
            token=dto.token,
            model=dto.model,
            length=dto.length,
        )
