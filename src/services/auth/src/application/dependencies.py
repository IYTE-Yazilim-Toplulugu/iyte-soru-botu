from fastapi import Depends
from shared_kernel import Mediator
from sqlmodel import Session

from src.infrastructure.data.database import get_session
from src.infrastructure.data.repositories import UserRepository
from src.infrastructure.services import TokenService

from .commands.forgot_password import (
    ForgotPasswordCommand,
    ForgotPasswordCommandHandler,
)
from .commands.login_user import (
    LoginCommand,
    LoginCommandHandler,
)
from .commands.refresh_session import (
    RefreshSessionCommand,
    RefreshSessionCommandHandler,
)
from .commands.register_user import (
    RegisterCommand,
    RegisterCommandHandler,
)
from .commands.reset_password import (
    ResetPasswordCommand,
    ResetPasswordCommandHandler,
)
from .commands.verify_email import (
    VerifyEmailCommand,
    VerifyEmailCommandHandler,
)
from .queries.get_user import (
    GetUserQuery,
    GetUserQueryHandler,
)


def get_mediator(session: Session = Depends(get_session)) -> Mediator:
    """Get mediator instance with registered handlers."""
    mediator = Mediator()

    # Create dependencies
    user_repository = UserRepository(session)
    token_service = TokenService()

    # Create handlers with dependencies
    register_handler = RegisterCommandHandler(user_repository, token_service)
    login_handler = LoginCommandHandler(user_repository, token_service)
    forgot_password_handler = ForgotPasswordCommandHandler(user_repository)
    reset_password_handler = ResetPasswordCommandHandler(user_repository)
    verify_email_handler = VerifyEmailCommandHandler(user_repository)
    refresh_session_handler = RefreshSessionCommandHandler(user_repository, token_service)
    get_user_handler = GetUserQueryHandler(user_repository)

    # Register handlers to mediator
    mediator.register(RegisterCommand, register_handler)
    mediator.register(LoginCommand, login_handler)
    mediator.register(ForgotPasswordCommand, forgot_password_handler)
    mediator.register(ResetPasswordCommand, reset_password_handler)
    mediator.register(VerifyEmailCommand, verify_email_handler)
    mediator.register(RefreshSessionCommand, refresh_session_handler)
    mediator.register(GetUserQuery, get_user_handler)

    return mediator
