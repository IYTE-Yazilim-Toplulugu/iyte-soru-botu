from shared_kernel import (
    ApiResponse,
    IMapper,
    IRequestHandler,
    IValidator,
)
from src.domain.exceptions import InvalidCredentialsException, UserInactiveException
from src.domain.interfaces import (
    ITokenService,
    IUserRepository,
)
from src.domain.models import TokenResult
from ulid import ULID

from .command import LoginCommand


class LoginCommandHandler(IRequestHandler[LoginCommand, ApiResponse[TokenResult]]):
    """Handler for user login."""

    def __init__(
        self,
        repository: IUserRepository,
        validator: IValidator,
        mapper: IMapper,
        token_service: ITokenService,
    ):
        super().__init__(repository, validator, mapper)
        self._token_service = token_service

    async def handle(self, command: LoginCommand) -> ApiResponse[TokenResult]:
        """Handle user login."""
        # Find user by email
        user = await self._repository.find_by_email(command.email)
        if not user:
            raise InvalidCredentialsException()

        # Verify password
        if not user.verify_password(command.password):
            raise InvalidCredentialsException()

        # Check if user is active
        if not user.is_active:
            raise UserInactiveException()

        # Update last login
        user.update_last_login()
        await self._repository.update(user)

        # Generate tokens
        access_token = self._token_service.create_access_token(
            {"sub": user.id, "email": str(user.email)}
        )
        refresh_token = self._token_service.create_refresh_token({"sub": user.id})
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
