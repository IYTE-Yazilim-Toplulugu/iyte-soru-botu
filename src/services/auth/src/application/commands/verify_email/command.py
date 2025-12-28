from dataclasses import dataclass

from shared_kernel import ApiResponse, IRequest


@dataclass
class VerifyEmailCommand(IRequest[ApiResponse[None]]):
    """Command to verify user email."""

    token: str
