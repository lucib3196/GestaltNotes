from .notes import router
from .user import router as user_router
from .course import router as course_router
from .thread import router as thread_router


ALL_ROUTES = [router, user_router, course_router, thread_router]
