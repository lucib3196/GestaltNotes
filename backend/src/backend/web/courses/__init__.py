from .access_codes import router as access_code_router
from .courses import router as course_router
from .enrollments import router as enrollment_router

course_routes = [
    course_router,
    access_code_router,
    enrollment_router,
]
