from .course import router as course_router
from .healtcheck import router as health_router
from .notes import router
from .thread import router as thread_router
from .user import user_routes

ALL_ROUTES = [router, course_router, thread_router, health_router] + user_routes
