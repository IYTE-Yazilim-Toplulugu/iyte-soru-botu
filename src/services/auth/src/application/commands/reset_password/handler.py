from shared_kernel import ApiResponse, IRequestHandler
from src.domain.exceptions import InvalidTokenException
from src.domain.interfaces import IUserRepository

from .command import ResetPasswordCommand


class ResetPasswordCommandHandler(
    IRequestHandler[ResetPasswordCommand, ApiResponse[None]]
):
    """Handler for password reset."""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def handle(self, command: ResetPasswordCommand) -> ApiResponse[None]:
        """Handle password reset."""
        user = await self._user_repository.find_by_reset_token(command.token)
        if not user:
            raise InvalidTokenException("Invalid or expired reset token")

        user.change_password(command.new_password)
        await self._user_repository.update(user)

        return ApiResponse[None].success()
