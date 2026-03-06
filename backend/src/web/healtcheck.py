from src.core.settings import get_settings
from fastapi.routing import APIRouter

router = APIRouter(prefix="/health", tags=["healt"])

settings = get_settings()


@router.get("/")
def get_origins():
    return {"data": settings.BACKEND_CORS_ORIGINS}
