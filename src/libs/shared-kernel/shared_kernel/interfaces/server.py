from abc import ABC
from typing import (
    List,
    Optional,
)

from fastapi import FastAPI
from pydantic_settings import BaseSettings
from starlette.middleware.cors import CORSMiddleware

from .route import Route


class App(ABC):
    app: FastAPI

    def __init__(
        self,
        routes: Optional[List[Route]] = None,
        settings: Optional[BaseSettings] = None,
    ):
        self.settings = settings
        self.app = FastAPI(title=settings.PROJECT_NAME)
        self.initializeRoutes(routes)
        self.initializeBuiltMiddlewares()

    def initializeRoutes(self, routes: List[Route]):

        if not routes:
            return

        for route in routes:
            self.app.include_router(route.router, prefix=self.settings.API_V1_STR)

    def initializeBuiltMiddlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin) for origin in self.settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
