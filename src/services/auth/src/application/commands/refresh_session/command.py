from dataclasses import dataclass

from shared_kernel import ApiResponse, IRequest
from src.domain.models import TokenResult


@dataclass
class RefreshSessionCommand(IRequest[ApiResponse[TokenResult]]):
    """Command to refresh access token using refresh token."""

    refresh_token: str
