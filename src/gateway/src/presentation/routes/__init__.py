from .auth_proxy import router as auth_router
from .chat_proxy import router as chat_router
from .document_proxy import router as document_router
from .health import router as health_router

__all__ = ["auth_router", "chat_router", "document_router", "health_router"]
