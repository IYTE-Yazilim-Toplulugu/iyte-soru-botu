from datetime import datetime
from typing import Optional

from sqlmodel import (
    Field,
    SQLModel,
)


class EmbeddingDbModel(SQLModel, table=True):
    __tablename__ = "embeddings"

    id: Optional[str] = Field(default=None, primary_key=True)
    vector: str  # JSON string of vector
    model: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
