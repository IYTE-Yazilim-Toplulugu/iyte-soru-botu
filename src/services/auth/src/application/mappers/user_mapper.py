from shared_kernel import IMapper
from src.domain.entities import User
from src.domain.value_objects import (
    Email,
    HashedPassword,
)
from src.infrastructure.data.models import UserDbModel
from ulid import ULID

from ..dtos import UserDTO


class UserMapper(IMapper[UserDbModel, User, UserDTO]):
    """Mapper for User entity, database model, and DTO."""

    def to_domain(self, db_model: UserDbModel) -> User:
        """Map database model to domain entity."""
        return User(
            id=ULID(db_model.id),
            email=Email(db_model.email),
            hashed_password=HashedPassword(db_model.hashed_password),
            first_name=db_model.first_name,
            last_name=db_model.last_name,
            is_active=db_model.is_active,
            is_verified=db_model.is_verified,
            verification_token=db_model.verification_token,
            reset_token=db_model.reset_token,
            last_login=db_model.last_login,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at,
        )

    def to_db(self, domain_entity: User) -> UserDbModel:
        """Map domain entity to database model."""
        return UserDbModel(
            id=str(domain_entity.id),
            email=str(domain_entity.email),
            hashed_password=domain_entity.hashed_password.value,
            first_name=domain_entity.first_name,
            last_name=domain_entity.last_name,
            is_active=domain_entity.is_active,
            is_verified=domain_entity.is_verified,
            verification_token=domain_entity.verification_token,
            reset_token=domain_entity.reset_token,
            last_login=domain_entity.last_login,
            created_at=domain_entity.created_at,
            updated_at=domain_entity.updated_at,
        )

    def to_db_update(self, domain_entity: User, db_model: UserDbModel) -> UserDbModel:
        """Update database model with domain entity values."""
        db_model.email = str(domain_entity.email)
        db_model.hashed_password = domain_entity.hashed_password.value
        db_model.first_name = domain_entity.first_name
        db_model.last_name = domain_entity.last_name
        db_model.is_active = domain_entity.is_active
        db_model.is_verified = domain_entity.is_verified
        db_model.verification_token = domain_entity.verification_token
        db_model.reset_token = domain_entity.reset_token
        db_model.last_login = domain_entity.last_login
        db_model.updated_at = domain_entity.updated_at
        return db_model

    def to_dto(self, domain_entity: User) -> UserDTO:
        """Map domain entity to DTO."""
        return UserDTO(
            id=str(domain_entity.id),
            email=str(domain_entity.email),
            first_name=domain_entity.first_name,
            last_name=domain_entity.last_name,
            is_active=domain_entity.is_active,
            is_verified=domain_entity.is_verified,
        )

    def from_dto(self, dto: UserDTO) -> User:
        """Map DTO to domain entity."""

        raise NotImplementedError(
            "Cannot create User entity from DTO directly. Use User.create() factory method."
        )
