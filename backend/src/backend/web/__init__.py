from .accounts import account_routes
from .annoucements.admin import router as announcement_admin_router
from .annoucements.announcements import router as announcements_router
from .chat.thread import router as thread_router
from .courses import course_routes
from .generated_content.mcq import router as mcq_router
from .health.health import router as health_router
from .processing import processing_routes
from .storage.files import router as files_router

ALL_ROUTES = [
    announcements_router,
    announcement_admin_router,
    files_router,
    *course_routes,
    thread_router,
    health_router,
    mcq_router,
    health_router,
    *account_routes,
    *processing_routes,
]
