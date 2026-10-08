from .chat.thread import router as thread_router
from .course import router as course_router
from .generated_content.mcq import router as mcq_router
from .notes import router
from .user import user_routes
from .health.health import router as health_router

ALL_ROUTES = [
    router,
    course_router,
    thread_router,
    health_router,
    mcq_router,
    *user_routes,
    health_router
]
