from dataclasses import dataclass

from shared_kernel import (
    ApiResponse,
    IRequest,
)


@dataclass
class RegisterCommand(IRequest[ApiResponse[dict[str, str]]]):
    """Command to register a new user."""

    email: str
    password: str
