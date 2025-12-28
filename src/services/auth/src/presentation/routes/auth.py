from fastapi import (
    APIRouter,
    Depends,
)
from shared_kernel import (
    ApiResponse,
    Mediator,
)
from shared_kernel import Route as RouteInstance
from src.application.commands.forgot_password import ForgotPasswordCommand
from src.application.commands.login_user import LoginCommand
from src.application.commands.refresh_session import RefreshSessionCommand
from src.application.commands.register_user import RegisterCommand
from src.application.commands.reset_password import ResetPasswordCommand
from src.application.commands.verify_email import VerifyEmailCommand
from src.application.dependencies import get_mediator
from src.domain.models import TokenResult


class AuthRouter(RouteInstance):

    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.setup_routes()

    def setup_routes(self):

        self.router.add_api_route(
            path="/register",
            endpoint=self._register_user,
            methods=["POST"],
            response_model=ApiResponse[TokenResult],
            status_code=201,
        )

        self.router.add_api_route(
            path="/login",
            endpoint=self._login_user,
            methods=["POST"],
            response_model=ApiResponse[TokenResult],
            status_code=200,
        )

        self.router.add_api_route(
            path="/forgot-password",
            endpoint=self._forgot_password,
            methods=["POST"],
            response_model=ApiResponse[None],
            status_code=200,
        )

        self.router.add_api_route(
            path="/reset-password",
            endpoint=self._reset_password,
            methods=["POST"],
            response_model=ApiResponse[None],
            status_code=200,
        )

        self.router.add_api_route(
            path="/refresh",
            endpoint=self._refresh_session,
            methods=["POST"],
            response_model=ApiResponse[TokenResult],
            status_code=200,
        )

        self.router.add_api_route(
            path="/verify-email",
            endpoint=self._verify_email,
            methods=["POST"],
            response_model=ApiResponse[None],
            status_code=200,
        )

    @staticmethod
    async def _register_user(
        command: RegisterCommand, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[TokenResult]:
        return await mediator.send(command)

    @staticmethod
    async def _login_user(
        command: LoginCommand, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[TokenResult]:
        return await mediator.send(command)

    @staticmethod
    async def _forgot_password(
        command: ForgotPasswordCommand, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[None]:
        return await mediator.send(command)

    @staticmethod
    async def _reset_password(
        command: ResetPasswordCommand, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[None]:
        return await mediator.send(command)

    @staticmethod
    async def _refresh_session(
        command: RefreshSessionCommand, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[TokenResult]:
        return await mediator.send(command)

    @staticmethod
    async def _verify_email(
        command: VerifyEmailCommand, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[None]:
        return await mediator.send(command)
