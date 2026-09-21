from fastapi.routing import APIRouter

from backend.core.settings import get_settings

router = APIRouter(prefix="/health", tags=["health"])

settings = get_settings()


@router.get("/")
def get_origins():
    return {"data": settings.BACKEND_CORS_ORIGINS}
