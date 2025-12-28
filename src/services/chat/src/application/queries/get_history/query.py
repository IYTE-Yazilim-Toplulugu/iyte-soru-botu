from dataclasses import dataclass
from typing import (
    List,
    Optional,
)

from shared_kernel import (
    ApiResponse,
    IRequest,
)

from src.domain.entities import Message


@dataclass
class GetHistoryQuery(IRequest[ApiResponse[List[Message]]]):
    chat_id: str
    user_id: str
    limit: Optional[int] = None
