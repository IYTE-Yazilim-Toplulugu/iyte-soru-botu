from dataclasses import dataclass

from shared_kernel import (
    ApiResponse,
    IRequest,
)

from ...dtos import UserDTO


@dataclass
class LoginCommand(IRequest[ApiResponse[UserDTO]]):
    email: str
    password: str
