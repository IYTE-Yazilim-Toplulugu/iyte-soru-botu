from fastapi import (
    APIRouter,
    Depends,
)
from shared_kernel import (
    ApiResponse,
    Mediator,
)
from shared_kernel import Route as RouteInstance

# from src.application.commands.deactivate_user import DeactivateUserCommand
# from src.application.commands.update_user import UpdateUserCommand
from src.application.dependencies import get_mediator
from src.application.dtos import UserDTO
from src.application.queries.get_user import GetUserQuery


class UserRouter(RouteInstance):
    def __init__(self):
        self.router = APIRouter(prefix="/user", tags=["user"])
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route(
            path="/{user-id}",
            endpoint=self._get_user,
            methods=["GET"],
            response_model=ApiResponse[UserDTO],
            status_code=200,
        )

        # TODO: Implement deactivate and update user commands
        # self.router.add_api_route(
        #     path="/deactivate",
        #     endpoint=self._deactivate_user,
        #     methods=["DELETE"],
        #     response_model=ApiResponse[None],
        #     status_code=204,
        # )
        # self.router.add_api_route(
        #     path="/{user-id}",
        #     endpoint=self._update_user,
        #     methods=["PATCH"],
        #     response_model=ApiResponse[UserDTO],
        #     status_code=200,
        # )

    @staticmethod
    async def _get_user(
        query: GetUserQuery, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[UserDTO]:
        return await mediator.send(query)

    # @staticmethod
    # async def _deactivate_user(
    #     command: DeactivateUserCommand, mediator: Mediator = Depends(get_mediator)
    # ) -> ApiResponse[None]:
    #     return await mediator.send(command)

    # @staticmethod
    # async def _update_user(
    #     command: UpdateUserCommand, mediator: Mediator = Depends(get_mediator)
    # ) -> ApiResponse[UserDTO]:
    #     return await mediator.send(command)
