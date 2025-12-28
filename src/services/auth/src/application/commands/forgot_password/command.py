from dataclasses import dataclass

from shared_kernel import ApiResponse, IRequest


@dataclass
class ForgotPasswordCommand(IRequest[ApiResponse[None]]):
    """Command to initiate password reset."""

    email: str
