from .account import router as account_router
from .health import router as health_router
from .students import router as student_router

account_routes = [student_router, account_router, health_router]

__all__ = ["account_routes"]
