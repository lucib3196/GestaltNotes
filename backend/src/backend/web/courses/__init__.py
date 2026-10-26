from .access_codes import router as access_code_router
from .courses import router as course_router
from .enrollments import router as enrollment_router
from .note_blocks import router as note_blocks_router
from .notes import router as notes_router
from .processing_runs import router as processing_runs_router

course_routes = [
    course_router,
    access_code_router,
    enrollment_router,
    notes_router,
    note_blocks_router,
    processing_runs_router,
]
