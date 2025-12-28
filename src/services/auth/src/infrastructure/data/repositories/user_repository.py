from typing import Optional
from sqlmodel import Session, select

from src.application.mappers import UserMapper
from src.domain.entities import User
from src.domain.interfaces import IUserRepository
from ..models import UserDbModel


class UserRepository(IUserRepository):
    """Repository implementation for User aggregate."""

    def __init__(self, session: Session):
        self._session = session
        self._mapper = UserMapper()

    async def add(self, entity: User) -> None:
        """Add a new user."""
        db_model = self._mapper.to_db(entity)
        self._session.add(db_model)
        self._session.commit()
        self._session.refresh(db_model)

    async def get_by_id(self, id: str) -> Optional[User]:
        """Get a user by ID."""
        stmt = select(UserDbModel).where(UserDbModel.id == id)
        db_model = self._session.exec(stmt).first()
        return self._mapper.to_domain(db_model) if db_model else None

    async def update(self, entity: User) -> None:
        """Update a user."""
        stmt = select(UserDbModel).where(UserDbModel.id == entity.id)
        db_model = self._session.exec(stmt).first()
        if db_model:
            updated_model = self._mapper.to_db_update(entity, db_model)
            self._session.add(updated_model)
            self._session.commit()

    async def delete(self, id: str) -> None:
        """Delete a user."""
        stmt = select(UserDbModel).where(UserDbModel.id == id)
        db_model = self._session.exec(stmt).first()
        if db_model:
            self._session.delete(db_model)
            self._session.commit()

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        stmt = select(UserDbModel).where(UserDbModel.email == email)
        db_model = self._session.exec(stmt).first()
        return self._mapper.to_domain(db_model) if db_model else None

    async def exists_by_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        stmt = select(UserDbModel).where(UserDbModel.email == email)
        return self._session.exec(stmt).first() is not None

    async def find_by_reset_token(self, token: str) -> Optional[User]:
        """Find a user by reset token."""
        stmt = select(UserDbModel).where(UserDbModel.reset_token == token)
        db_model = self._session.exec(stmt).first()
        return self._mapper.to_domain(db_model) if db_model else None

    async def find_by_verification_token(self, token: str) -> Optional[User]:
        """Find a user by verification token."""
        stmt = select(UserDbModel).where(UserDbModel.verification_token == token)
        db_model = self._session.exec(stmt).first()
        return self._mapper.to_domain(db_model) if db_model else None
