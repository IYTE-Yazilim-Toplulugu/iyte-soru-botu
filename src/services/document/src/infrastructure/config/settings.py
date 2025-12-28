from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Document service configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # MongoDB
    MONGODB_URL: str = "mongodb://root:root@localhost:27017/"
    MONGODB_DATABASE: str = "document_db"

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "documents"
    MINIO_SECURE: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8082
    GRPC_PORT: int = 50051
    PROJECT_NAME: str = "document-service"
    API_V1_STR: str = "/api/v1/documents"


settings = Settings()
