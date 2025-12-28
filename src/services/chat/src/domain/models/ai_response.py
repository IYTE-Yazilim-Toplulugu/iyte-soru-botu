from dataclasses import dataclass

from pydantic import BaseModel

from ..enums import Model


@dataclass
class AIResponse(BaseModel):
    """
    Domain model representing an AI-generated response.
    """

    content: str
    token: int
    model: Model
