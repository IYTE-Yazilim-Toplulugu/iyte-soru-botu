from dataclasses import dataclass

from shared_kernel import ApiResponse, IRequest

from ...dtos import UserDTO


@dataclass
class GetUserQuery(IRequest[ApiResponse[UserDTO]]):
    """Query to get user by ID."""

    user_id: str
