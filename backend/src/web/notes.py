from fastapi.routing import APIRouter
from src.web.dependencies import FirebaseDependency

router = APIRouter(prefix="/notes")


@router.get("/")
async def get_notes(storage: FirebaseDependency):
    files = storage.list_files("Notes/ME135/Lecture_9_26_25")
    return files
