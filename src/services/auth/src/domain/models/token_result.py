from pydantic import BaseModel


class TokenResult(BaseModel):
    """Token result model."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    jti: str
