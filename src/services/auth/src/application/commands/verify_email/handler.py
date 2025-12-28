from shared_kernel import ApiResponse, IRequestHandler
from src.domain.exceptions import InvalidTokenException
from src.domain.interfaces import IUserRepository

from .command import VerifyEmailCommand


class VerifyEmailCommandHandler(
    IRequestHandler[VerifyEmailCommand, ApiResponse[None]]
):
    """Handler for email verification."""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def handle(self, command: VerifyEmailCommand) -> ApiResponse[None]:
        """Handle email verification."""
        user = await self._user_repository.find_by_verification_token(command.token)
        if not user:
            raise InvalidTokenException("Invalid or expired verification token")

        user.verify_email()
        await self._user_repository.update(user)

        return ApiResponse[None].success()
