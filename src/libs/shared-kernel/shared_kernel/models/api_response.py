from typing import (
    Generic,
    Optional,
    TypeVar,
)

from pydantic import BaseModel

from ..enums import ResponseCode
from .pagination import PagedResult

D = TypeVar("D")  # Data type


class ApiResponse(BaseModel, Generic[D]):
    """
    Generic API response that can handle any response type.
    Use D=None for responses without data.
    """

    code: ResponseCode
    message: Optional[str] = None
    data: Optional[D] = None

    @classmethod
    def success(
        cls, data: Optional[D] = None, message: Optional[str] = None
    ) -> "ApiResponse[D]":
        """Create a successful response."""
        return cls(code=ResponseCode.SUCCESS, message=message, data=data)

    @classmethod
    def internal_error(
        cls, message: str = "Internal server error."
    ) -> "ApiResponse[D]":
        """Create an internal error response."""
        return cls(code=ResponseCode.INTERNAL_ERROR, message=message, data=None)

    @classmethod
    def bad_request(cls, message: str = "Bad request.") -> "ApiResponse[D]":
        """Create a bad request response."""
        return cls(code=ResponseCode.BAD_REQUEST, message=message, data=None)

    @classmethod
    def unauthenticated(cls, message: str = "Unauthenticated.") -> "ApiResponse[D]":
        """Create an unauthenticated response."""
        return cls(code=ResponseCode.UNAUTHENTICATED, message=message, data=None)

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized.") -> "ApiResponse[D]":
        """Create an unauthorized response."""
        return cls(code=ResponseCode.UNAUTHORIZED, message=message, data=None)

    @classmethod
    def not_found(cls, message: str = "Not found.") -> "ApiResponse[D]":
        """Create a not found response."""
        return cls(code=ResponseCode.NOT_FOUND, message=message, data=None)

    @classmethod
    def exists(cls, message: str = "Already exists.") -> "ApiResponse[D]":
        """Create an exists response."""
        return cls(code=ResponseCode.EXISTS, message=message, data=None)

    @classmethod
    def forbidden(cls, message: str = "Forbidden.") -> "ApiResponse[D]":
        """Create a forbidden response."""
        return cls(code=ResponseCode.FORBIDDEN, message=message, data=None)

    @classmethod
    def service_specified(
        cls, message: str, data: Optional[D] = None
    ) -> "ApiResponse[D]":
        """Create a service-specific response."""
        return cls(code=ResponseCode.SERVICE_SPECIFIED, message=message, data=data)


T = TypeVar("T")  # Generic type for pagination


class PaginatedResponse(ApiResponse[PagedResult[T]]):
    """
    Specialized response for paginated data.
    Extends ApiResponse with pagination metadata.
    """

    page_number: int
    total_page: int
    total_count: int

    @classmethod
    def create(
        cls,
        data: PagedResult[T],
        page_number: int,
        total_page: int,
        total_count: int,
        message: Optional[str] = None,
    ) -> "PaginatedResponse[T]":
        """Create a successful paginated response with metadata."""
        return cls(
            code=ResponseCode.SUCCESS,
            message=message,
            data=data,
            page_number=page_number,
            total_page=total_page,
            total_count=total_count,
        )

    def has_previous_page(self) -> bool:
        """Check if there's a previous page."""
        return self.page_number > 1

    def has_next_page(self) -> bool:
        """Check if there's a next page."""
        return self.page_number < self.total_page
