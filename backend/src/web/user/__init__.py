from .health import router as health_router
from .user import router as user_router

user_routes = [user_router, health_router]
__all__ = ["user_routes"]
