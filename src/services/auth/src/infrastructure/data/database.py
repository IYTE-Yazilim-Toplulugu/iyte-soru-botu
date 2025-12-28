from contextlib import contextmanager
from typing import Generator

from sqlmodel import (
    Session,
    SQLModel,
    create_engine,
)

from ..config.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    with get_session() as session:
        yield session
