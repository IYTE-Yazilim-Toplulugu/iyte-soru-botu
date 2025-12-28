from abc import ABC, abstractmethod
from typing import Dict, Type

from fastapi import Request, status
from fastapi.responses import JSONResponse
from shared_kernel import ApiResponse, DomainException

from src.domain.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserInactiveException,
    UserNotFoundException,
)


class IExceptionMapper(ABC):
    """Interface for mapping exceptions to API responses."""

    @abstractmethod
    def map(self, exc: Exception) -> tuple[ApiResponse[None], int]:
        """Map exception to ApiResponse and HTTP status code."""
        pass


class DomainExceptionMapper(IExceptionMapper):
    """Maps domain exceptions to appropriate API responses."""

    def __init__(self):
        self._exception_map: Dict[Type[Exception], tuple[str, int]] = {
            UserAlreadyExistsException: (
                self._handle_user_exists,
                status.HTTP_409_CONFLICT,
            ),
            InvalidCredentialsException: (
                self._handle_invalid_credentials,
                status.HTTP_401_UNAUTHORIZED,
            ),
            UserNotFoundException: (
                self._handle_user_not_found,
                status.HTTP_404_NOT_FOUND,
            ),
            InvalidTokenException: (
                self._handle_invalid_token,
                status.HTTP_400_BAD_REQUEST,
            ),
            UserInactiveException: (
                self._handle_user_inactive,
                status.HTTP_403_FORBIDDEN,
            ),
        }

    def map(self, exc: Exception) -> tuple[ApiResponse[None], int]:
        """Map domain exception to ApiResponse."""
        exc_type = type(exc)

        if exc_type in self._exception_map:
            handler, status_code = self._exception_map[exc_type]
            return handler(exc), status_code

        # Default domain exception handling
        return ApiResponse[None].bad_request(str(exc)), status.HTTP_400_BAD_REQUEST

    @staticmethod
    def _handle_user_exists(exc: UserAlreadyExistsException) -> ApiResponse[None]:
        return ApiResponse[None].exists(str(exc))

    @staticmethod
    def _handle_invalid_credentials(
        exc: InvalidCredentialsException,
    ) -> ApiResponse[None]:
        return ApiResponse[None].unauthenticated(str(exc))

    @staticmethod
    def _handle_user_not_found(exc: UserNotFoundException) -> ApiResponse[None]:
        return ApiResponse[None].not_found(str(exc))

    @staticmethod
    def _handle_invalid_token(exc: InvalidTokenException) -> ApiResponse[None]:
        return ApiResponse[None].bad_request(str(exc))

    @staticmethod
    def _handle_user_inactive(exc: UserInactiveException) -> ApiResponse[None]:
        return ApiResponse[None].forbidden(str(exc))


class ValidationExceptionMapper(IExceptionMapper):
    """Maps validation exceptions to API responses."""

    def map(self, exc: Exception) -> tuple[ApiResponse[None], int]:
        """Map validation exception to ApiResponse."""
        return ApiResponse[None].bad_request(str(exc)), status.HTTP_400_BAD_REQUEST


class GenericExceptionMapper(IExceptionMapper):
    """Maps generic exceptions to API responses."""

    def map(self, exc: Exception) -> tuple[ApiResponse[None], int]:
        """Map generic exception to ApiResponse."""
        return (
            ApiResponse[None].internal_error("An unexpected error occurred"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class GlobalExceptionHandler:
    """Global exception handler for the application."""

    def __init__(self):
        self._domain_mapper = DomainExceptionMapper()
        self._validation_mapper = ValidationExceptionMapper()
        self._generic_mapper = GenericExceptionMapper()

    async def handle_domain_exception(
        self, request: Request, exc: DomainException
    ) -> JSONResponse:
        """Handle domain exceptions."""
        response, status_code = self._domain_mapper.map(exc)
        return JSONResponse(
            status_code=status_code,
            content=response.model_dump(),
        )

    async def handle_validation_exception(
        self, request: Request, exc: ValueError
    ) -> JSONResponse:
        """Handle validation exceptions."""
        response, status_code = self._validation_mapper.map(exc)
        return JSONResponse(
            status_code=status_code,
            content=response.model_dump(),
        )

    async def handle_generic_exception(
        self, request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle generic exceptions."""
        response, status_code = self._generic_mapper.map(exc)
        return JSONResponse(
            status_code=status_code,
            content=response.model_dump(),
        )


# Singleton instance
exception_handler = GlobalExceptionHandler()
