from .notes import router
from .user import router as user_router
ALL_ROUTES = [router, user_router]
