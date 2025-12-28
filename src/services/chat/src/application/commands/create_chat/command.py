from dataclasses import dataclass
from typing import Optional

from shared_kernel import (
    ApiResponse,
    IRequest,
)
from ulid import ULID

from ...dtos import ChatDTO


@dataclass
class CreateChatCommand(IRequest[ApiResponse[ChatDTO]]):

    user_id: ULID
    message: Optional[str] = None
