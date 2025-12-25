from dataclasses import dataclass
from typing import (
    Generic,
    TypeVar,
)

from pydantic import (
    BaseModel,
    Field,
)


@dataclass(frozen=True)
class PageRequest(BaseModel):
    """
    Represents a pagination request.

    Attributes:
        page: The page number (1-indexed).
        page_size: The number of items per page.
    """

    page: int = Field(..., ge=1, description="The page number (1-indexed).")
    page_size: int = Field(..., ge=1, description="The number of items per page.")

    @property
    def offset(self) -> int:
        """Calculate the offset for database queries."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get the limit for database queries."""
        return self.page_size


T = TypeVar("T")


@dataclass(frozen=True)
class PagedResult(BaseModel, Generic[T]):
    """
    Represents a paginated result set with validation.
    """

    items: tuple[T, ...]
    total_count: int = Field(
        ..., ge=0, description="Total number of items across all pages."
    )
    page: int = Field(..., ge=1, description="Current page number.")
    page_size: int = Field(..., ge=0, description="Number of items per page.")

    @property
    def total_pages(self) -> int:

        if self.total_count == 0:
            return 0
        if self.page_size == 0:
            return 0
        return (self.total_count + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @property
    def next_page(self) -> int | None:
        return self.page + 1 if self.has_next else None

    @property
    def previous_page(self) -> int | None:
        return self.page - 1 if self.has_previous else None
