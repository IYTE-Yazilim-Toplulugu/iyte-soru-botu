from shared_kernel.interfaces.mapper import IMapper

from src.application.dtos import ChatDTO
from src.domain.entities.chat import Chat

from ..models.chat_db_model import ChatDbModel


class ChatMapper(IMapper[ChatDbModel, Chat, ChatDTO]):
    def to_domain(self, db_model: ChatDbModel) -> Chat:
        return Chat(
            id=db_model.id,
            user_id=db_model.user_id,
            title=db_model.title,
            message_count=db_model.message_count,
            is_archived=db_model.is_archived,
            updated_at=db_model.updated_at,
        )

    def to_db(self, domain_entity: Chat) -> ChatDbModel:
        return ChatDbModel(
            id=domain_entity.id,
            user_id=domain_entity.user_id,
            title=domain_entity.title,
            message_count=domain_entity.message_count,
            is_archived=domain_entity.is_archived,
            updated_at=domain_entity.updated_at,
        )

    def to_db_update(self, domain_entity: Chat, db_model: ChatDbModel) -> ChatDbModel:
        db_model.user_id = domain_entity.user_id
        db_model.title = domain_entity.title
        db_model.message_count = domain_entity.message_count
        db_model.is_archived = domain_entity.is_archived
        db_model.updated_at = domain_entity.updated_at

        return db_model

    def to_dto(self, domain_entity: Chat) -> ChatDTO:
        return ChatDTO(
            id=domain_entity.id,
            user_id=domain_entity.user_id,
            title=domain_entity.title,
            message_count=domain_entity.message_count,
            is_archived=domain_entity.is_archived,
            updated_at=domain_entity.updated_at,
        )

    def from_dto(self, dto: ChatDTO) -> Chat:
        return Chat(
            id=dto.id,
            user_id=dto.user_id,
            title=dto.title,
            message_count=dto.message_count,
            is_archived=dto.is_archived,
            updated_at=dto.updated_at,
        )
