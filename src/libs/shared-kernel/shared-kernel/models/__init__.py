from .api_response import BasicResponse  # Deprecated in 0.4.0
from .api_response import DataResponse  # Deprecated in 0.4.0
from .api_response import (
    ApiResponse,
    PaginatedResponse,
)
from .pagination import (
    PagedResult,
    PageRequest,
)

__all__ = [
    "ApiResponse",
    "BasicResponse",  # Deprecated - use ApiResponse[None]
    "DataResponse",  # Deprecated - use ApiResponse[D]
    "PaginatedResponse",
    "PageRequest",
    "PagedResult",
]
