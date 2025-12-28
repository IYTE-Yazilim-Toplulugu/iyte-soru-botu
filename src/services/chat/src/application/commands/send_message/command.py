from dataclasses import dataclass
from typing import Optional

from shared_kernel import (
    ApiResponse,
    IRequest,
)
from ulid import ULID

from ...dtos import MessageDTO


@dataclass
class SendMessageCommand(IRequest[ApiResponse[MessageDTO]]):
    chat_id: ULID
    user_id: str
    content: str
    generate_ai_response: bool = True
    model: Optional[str] = None
