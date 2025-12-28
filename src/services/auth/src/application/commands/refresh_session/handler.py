from ulid import ULID

from shared_kernel import ApiResponse, IRequestHandler
from src.domain.exceptions import InvalidTokenException, UserNotFoundException
from src.domain.interfaces import ITokenService, IUserRepository
from src.domain.models import TokenResult

from .command import RefreshSessionCommand


class RefreshSessionCommandHandler(
    IRequestHandler[RefreshSessionCommand, ApiResponse[TokenResult]]
):
    """Handler for refreshing session tokens."""

    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
    ):
        self._user_repository = user_repository
        self._token_service = token_service

    async def handle(self, command: RefreshSessionCommand) -> ApiResponse[TokenResult]:
        """Handle token refresh."""
        # Verify refresh token
        payload = self._token_service.verify_token(command.refresh_token)

        # Check token type
        if payload.get("type") != "refresh":
            raise InvalidTokenException("Invalid token type")

        # Get user
        user_id = payload.get("sub")
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)

        # Check if user is active
        if not user.is_active:
            raise InvalidTokenException("User account is inactive")

        # Generate new tokens
        access_token = self._token_service.create_access_token(
            {"sub": str(user.id), "email": str(user.email)}
        )
        new_refresh_token = self._token_service.create_refresh_token(
            {"sub": str(user.id)}
        )
        jti = str(ULID())

        token_result = TokenResult(
            access_token=access_token,
            token_type="Bearer",
            expires_in=3600,
            refresh_token=new_refresh_token,
            scope="read write",
            jti=jti,
        )

        return ApiResponse[TokenResult].success(data=token_result)
