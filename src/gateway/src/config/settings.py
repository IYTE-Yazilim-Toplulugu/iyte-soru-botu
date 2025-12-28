from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Gateway service configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    PROJECT_NAME: str = "IYTE Soru Botu Gateway"
    API_VERSION: str = "v1"

    # Service URLs
    AUTH_SERVICE_URL: str = "http://auth-service:8081"
    CHAT_SERVICE_URL: str = "http://chat-service:8080"
    DOCUMENT_SERVICE_URL: str = "http://document-service:8082"

    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    SESSION_EXPIRE_SECONDS: int = 3600  # 1 hour

    # Security
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
    ]

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100  # requests
    RATE_LIMIT_WINDOW: int = 60  # seconds


settings = Settings()
