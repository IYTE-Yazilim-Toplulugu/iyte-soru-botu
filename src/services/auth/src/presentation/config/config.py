import secrets
from typing import (
    Annotated,
    Any,
    Literal,
    Optional,
)

from pydantic import (
    AnyHttpUrl,
    BeforeValidator,
    EmailStr,
)
from pydantic_settings import BaseSettings


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    PROJECT_NAME: str = "chat-service"
    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = []

    # Environment
    ENV: Literal["development", "production", "test"] = "development"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE: int = 3600
    REFRESH_TOKEN_EXPIRE: int = 3600 * 24 * 30
    JWT_ALGO: str = "RS256"
    ACCESSTOKENPUBLICKEY: str = ""
    ACCESSTOKENPRIVATEKEY: str = ""
    REFRESHTOKENPUBLICKEY: str = ""
    REFRESHTOKENPRIVATEKEY: str = ""

    # SMTP / Emails
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAILS_ENABLED: bool = True
    EMAILS_DIRECTORY: str = "app/templates/"
    FRONTEND_MAIN_ORIGIN: str = "http://localhost:3000"

    # Mongo
    MONGO_USER: str = ""
    MONGO_PASS: str = ""
    MONGO_HOST: str = "localhost"
    MONGO_PORT: str = "27017"
    DB_NAME: str = ""

    @property
    def MONGO_URI(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.DB_NAME}?authSource=admin"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


TOKEN_PARAMS = {
    "ACCESSTOKENPUBLICKEY": settings.ACCESSTOKENPUBLICKEY,
    "ACCESSTOKENPRIVATEKEY": settings.ACCESSTOKENPRIVATEKEY,
    "REFRESHTOKENPRIVATEKEY": settings.REFRESHTOKENPRIVATEKEY,
    "REFRESHTOKENPUBLICKEY": settings.REFRESHTOKENPUBLICKEY,
}
