from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from shared_kernel import (
    ApiResponse,
    Mediator,
)
from shared_kernel import Route as RouteInstance
from src.application.commands.create_chat import CreateChatCommand
from src.application.dependencies import get_mediator
from src.application.dtos import (
    ChatDTO,
    MessageDTO,
)
from src.application.queries.get_history import GetHistoryQuery


class ChatRouter(RouteInstance):

    def __init__(self):
        self.router = APIRouter(tags=["chat"])
        self.setup_routes()

    def setup_routes(self):

        self.router.add_api_route(
            path="/create",
            endpoint=self._create_chat,
            methods=["POST"],
            response_model=ApiResponse[ChatDTO],
            status_code=201,
        )

        self.router.add_api_route(
            path="/send-message",
            endpoint=self._send_message,
            methods=["POST"],
            response_model=ApiResponse[MessageDTO],
            status_code=201,
        )

        self.router.add_api_route(
            path="/{chat_id}/messages",
            endpoint=self._get_history,
            methods=["GET"],
            response_model=ApiResponse[List[MessageDTO]],
            status_code=200,
        )

        # self.router.add_api_route(
        #     path="/",
        #     endpoint=self._get_chats,
        #     methods=["GET"],
        #     response_model=ApiResponse[List[ChatDTO]],
        # )

        # self.router.add_api_route(
        #     path="/{id}",
        #     endpoint=self._get_chat,
        #     methods=["GET"],
        #     response_model=GetChatResponse,
        # )
        #
        # self.router.add_api_route(
        #     path="/",
        #     endpoint=self._get_chats,
        #     methods=["GET"],
        #     response_model=GetAllChatsResponse,
        # )

    # @staticmethod
    # async def _get_chats(query: GetAllChatsQuery, mediator: Mediator = Depends(get_mediator)) -> GetAllChatsResponse:
    #     result = await mediator.send(query)
    #     return GetAllChatsResponse.from_entity(result)

    @staticmethod
    async def _get_history(
        query: GetHistoryQuery, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[List[MessageDTO]]:
        return await mediator.send(query)
        # return ApiResponse[List[MessageDTO]](data=result)

    @staticmethod
    async def _create_chat(
        command: CreateChatCommand, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[ChatDTO]:
        return await mediator.send(command)

    @staticmethod
    async def _send_message(
        command: CreateChatCommand, mediator: Mediator = Depends(get_mediator)
    ) -> ApiResponse[MessageDTO]:
        return await mediator.send(command)

    # @staticmethod
    # async def _get_chat(
    #     query: GetChatQuery, mediator: Mediator = Depends(get_mediator)
    # ) -> GetChatResponse:
    #     result = await mediator.send(query)
    #     return GetChatResponse.from_entity(result)
    #
    # @staticmethod
    # async def _get_all_chats(
    #     query: GetAllChatsQuery, mediator: Mediator = Depends(get_mediator)
    # ) -> GetChatResponse:
    #     result = await mediator.send(query)
    #     return GetChatResponse.from_entity(result)
