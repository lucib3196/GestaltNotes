from .runs import router as runs_router
from .tasks import router as tasks_router

processing_routes = [runs_router, tasks_router]

__all__ = ["processing_routes"]
