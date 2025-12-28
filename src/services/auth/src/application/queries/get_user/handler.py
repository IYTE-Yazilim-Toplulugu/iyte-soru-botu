from shared_kernel import ApiResponse, IRequestHandler
from src.application.mappers import UserMapper
from src.domain.exceptions import UserNotFoundException
from src.domain.interfaces import IUserRepository

from ...dtos import UserDTO
from .query import GetUserQuery


class GetUserQueryHandler(IRequestHandler[GetUserQuery, ApiResponse[UserDTO]]):
    """Handler for get user query."""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository
        self._mapper = UserMapper()

    async def handle(self, query: GetUserQuery) -> ApiResponse[UserDTO]:
        """Handle get user query."""
        user = await self._user_repository.get_by_id(query.user_id)
        if not user:
            raise UserNotFoundException(query.user_id)

        user_dto = self._mapper.to_dto(user)
        return ApiResponse[UserDTO].success(data=user_dto)
