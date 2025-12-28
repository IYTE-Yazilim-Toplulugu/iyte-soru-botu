from typing import Optional
import jwt
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config.settings import settings
from src.infrastructure.cache.redis_client import redis_cache


security = HTTPBearer()


class AuthMiddleware:
    """Authentication middleware for JWT token verification."""

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials,
    ) -> dict:
        """Get current user from token."""
        token = credentials.credentials

        # Check cache first
        cache_key = f"user:token:{token}"
        cached_user = await redis_cache.get(cache_key)
        if cached_user:
            return cached_user

        # Verify token
        payload = AuthMiddleware.verify_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        # Cache user data
        user_data = {
            "user_id": user_id,
            "email": payload.get("email"),
        }
        await redis_cache.set(cache_key, user_data, expire_seconds=300)  # 5 min

        return user_data

    @staticmethod
    def extract_token_from_header(request: Request) -> Optional[str]:
        """Extract token from Authorization header."""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        return parts[1]
