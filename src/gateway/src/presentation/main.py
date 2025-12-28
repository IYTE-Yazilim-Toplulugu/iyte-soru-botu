import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.infrastructure.cache.redis_client import redis_cache
from src.presentation.routes import (
    auth_router,
    chat_router,
    document_router,
    health_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    await redis_cache.connect()
    yield
    # Shutdown
    await redis_cache.disconnect()


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include health router (no prefix)
app.include_router(health_router)

# Include API routers with version prefix
api_prefix = f"/api/{settings.API_VERSION}"
app.include_router(auth_router, prefix=api_prefix)
app.include_router(chat_router, prefix=api_prefix)
app.include_router(document_router, prefix=api_prefix)


if __name__ == "__main__":
    uvicorn.run(
        "src.presentation.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
