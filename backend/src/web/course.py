from .dependencies import CourseDBDependency, EducatorDep
from src.core.database_config import SessionDep
from src.model.course import Course, CourseData, LectureNote, LectureNoteCreate
from fastapi.routing import APIRouter
from uuid import UUID
from sqlmodel import select
from fastapi import HTTPException
from fastapi.responses import Response

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/")
async def create_course(cdb: CourseDBDependency, data: CourseData) -> Course:
    return await cdb.create_course(data)


@router.get("/get_prof_courses", response_model=list[CourseData])
def get_my_courses(educator: EducatorDep):
    return educator.courses


@router.get("/{id}")
async def get_course(cdb: CourseDBDependency, id: str | UUID):
    return await cdb.get_course(id)

@router.post("/{course_id}/notes")
def upload_lecture_note(
    course_id: UUID,
    educator: EducatorDep,
    data: LectureNoteCreate,
    session: SessionDep,
):
    note = LectureNote(
        course_id=course_id,
        title=data.title,
        file_name=data.file_name,
        file_url=data.file_url,
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