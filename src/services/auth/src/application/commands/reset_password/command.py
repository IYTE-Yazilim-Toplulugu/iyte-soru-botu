from dataclasses import dataclass

from shared_kernel import ApiResponse, IRequest


@dataclass
class ResetPasswordCommand(IRequest[ApiResponse[None]]):
    """Command to reset user password with token."""

    token: str
    new_password: str
