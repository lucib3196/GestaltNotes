from fastapi.routing import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from src.web.dependencies import FbStorageDependency, EducatorDep, SessionDep
from src.model.course import LectureNote
from sqlmodel import select
from uuid import UUID
from pathlib import Path

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

@router.post("/{course_id}")
async def upload_lecture_note(
    course_id: UUID,
    educator: EducatorDep,
    session: SessionDep,
    storage: FbStorageDependency,
    file: UploadFile = File(...),
):
    allowed = {".pdf", ".pptx", ".docx"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"File type {ext} not allowed")

    contents = await file.read()
    path = f"courses/{course_id}/notes/{file.filename}"
    file_url = storage.upload_file(path, contents, file.content_type)

    note = LectureNote(
        course_id=course_id,
        title=file.filename.rsplit(".", 1)[0].replace("-", " ").replace("_", " "),
        file_name=file.filename,
        file_url=file_url,
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@router.delete("/{course_id}/{note_id}")
def delete_lecture_note(
    course_id: UUID,
    note_id: UUID,
    educator: EducatorDep,
    session: SessionDep,
    storage: FbStorageDependency,
):
    note = session.exec(select(LectureNote).where(LectureNote.id == note_id)).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    storage.delete_file(f"courses/{course_id}/notes/{note.file_name}")
    session.delete(note)
    session.commit()
    return Response(status_code=204)