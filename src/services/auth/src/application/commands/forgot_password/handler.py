import secrets
from datetime import datetime

from shared_kernel import ApiResponse, IRequestHandler
from src.domain.interfaces import IUserRepository

from .command import ForgotPasswordCommand


class ForgotPasswordCommandHandler(
    IRequestHandler[ForgotPasswordCommand, ApiResponse[None]]
):
    """Handler for forgot password command."""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def handle(self, command: ForgotPasswordCommand) -> ApiResponse[None]:
        """Handle forgot password command."""
        user = await self._user_repository.find_by_email(command.email)

        # Don't reveal if user exists or not for security
        if not user:
            return ApiResponse[None].success()

        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        user.reset_token = reset_token
        user.updated_at = datetime.utcnow()

        await self._user_repository.update(user)

        # TODO: Send email with reset token
        # email_service.send_password_reset_email(user.email, reset_token)

        return ApiResponse[None].success()
