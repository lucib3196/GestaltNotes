from .tasks import router as tasks_router

processing_routes = [tasks_router]

__all__ = ["processing_routes"]
