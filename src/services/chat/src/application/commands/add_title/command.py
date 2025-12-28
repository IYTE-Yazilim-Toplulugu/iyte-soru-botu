from dataclasses import dataclass

from shared_kernel import (
    ApiResponse,
    IRequest,
)
from ulid import ULID


@dataclass
class AddTitleCommand(IRequest[ApiResponse[None]]):
    user_id: ULID
    chat_id: ULID
    title: str
