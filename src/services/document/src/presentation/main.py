import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.infrastructure.config.settings import settings
from src.infrastructure.data.mongodb import mongodb_client
from src.presentation.routes import documents_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    await mongodb_client.connect()
    yield
    # Shutdown
    await mongodb_client.disconnect()


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": settings.PROJECT_NAME, "status": "running"}


if __name__ == "__main__":
    uvicorn.run(
        "src.presentation.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
