from ulid import ULID

from shared_kernel import ApiResponse, IRequestHandler
from src.domain.entities import User
from src.domain.exceptions import UserAlreadyExistsException
from src.domain.interfaces import (
    ITokenService,
    IUserRepository,
)
from src.domain.models import TokenResult

from .command import RegisterCommand


class RegisterCommandHandler(
    IRequestHandler[RegisterCommand, ApiResponse[TokenResult]]
):
    """Handler for user registration."""

    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
    ):
        self._user_repository = user_repository
        self._token_service = token_service

    async def handle(self, command: RegisterCommand) -> ApiResponse[TokenResult]:
        """Handle user registration."""
        # Check if user already exists
        if await self._user_repository.exists_by_email(command.email):
            raise UserAlreadyExistsException(command.email)

        # Create new user
        user = User.create(
            email=command.email,
            password=command.password,
        )

        # Save user
        await self._user_repository.add(user)

        # Generate tokens
        access_token = self._token_service.create_access_token(
            {"sub": str(user.id), "email": str(user.email)}
        )
        refresh_token = self._token_service.create_refresh_token({"sub": str(user.id)})
        jti = str(ULID())

        token_result = TokenResult(
            access_token=access_token,
            token_type="Bearer",
            expires_in=3600,
            refresh_token=refresh_token,
            scope="read write",
            jti=jti,
        )

        return ApiResponse[TokenResult].success(data=token_result)
