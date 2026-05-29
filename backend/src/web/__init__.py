from .course import router as course_router
from .healtcheck import router as health_router
from .notes import router
from .chat.thread import router as thread_router
from .user import user_routes
from .generated_content.mcq import router as mcq_router

ALL_ROUTES = [
    router,
    course_router,
    thread_router,
    health_router,
    mcq_router,
] + user_routes
