from pathlib import Path
from uuid import UUID

from fastapi import File, HTTPException, UploadFile
from fastapi.responses import Response
from fastapi.routing import APIRouter
from sqlmodel import select

from src.core.database_config import SessionDep
from src.model.course import Course, CourseData, LectureNote

from .dependencies import CourseDBDependency, FbStorageDependency
from src.web.user.dependencies import EducatorDep

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/")
async def create_course(cdb: CourseDBDependency, data: CourseData) -> Course:
    return await cdb.create_course(data)


@router.get("/get_prof_courses", response_model=list[Course])
def get_my_courses(educator: EducatorDep):
    return educator.courses


@router.get("/{id}")
async def get_course(cdb: CourseDBDependency, id: str | UUID):
    return await cdb.get_course(id)


@router.post("/{course_id}")
async def upload_lecture_note(
    course_id: UUID,
    educator: EducatorDep,
    session: SessionDep,
    storage: FbStorageDependency,
    file: UploadFile = File(...),
):
    # validate file type
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


@router.delete("/{course_id}/notes/{note_id}")
def delete_lecture_note(
    course_id: UUID,
    note_id: UUID,
    educator: EducatorDep,
    session: SessionDep,
):
    note = session.exec(select(LectureNote).where(LectureNote.id == note_id)).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return Response(status_code=204)
