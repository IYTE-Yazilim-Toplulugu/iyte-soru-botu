from shared_kernel import DomainException


class InvalidCredentialsException(DomainException):
    """Raised when user provides invalid credentials."""

    def __init__(self):
        super().__init__("Invalid email or password")


class UserAlreadyExistsException(DomainException):
    """Raised when attempting to create a user that already exists."""

    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists")


class UserNotFoundException(DomainException):
    """Raised when a user is not found."""

    def __init__(self, identifier: str):
        super().__init__(f"User not found: {identifier}")


class InvalidTokenException(DomainException):
    """Raised when a token is invalid or expired."""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)


class UserInactiveException(DomainException):
    """Raised when a user account is inactive."""

    def __init__(self, message: str = "User account is inactive"):
        super().__init__(message)
