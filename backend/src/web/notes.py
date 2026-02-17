from fastapi.routing import APIRouter
from src.web.dependencies import FbStorageDependency
from fastapi.responses import Response

router = APIRouter(prefix="/notes")

exclude = "output.json"


@router.get("/")
async def get_notes(storage: FbStorageDependency):
    files = storage.list_files("Notes/ME135/Lecture_9_26_25")
    filtered = [f for f in files if f.endswith(".md") or f.endswith(".pdf")]
    return filtered


@router.get("/test")
async def get_test_note(storage: FbStorageDependency):
    file = storage.read_file("Notes/ME135/Lecture_9_26_25/9-26-25.pdf")
    return Response(
        content=file,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=lecture1.pdf"},
    )
