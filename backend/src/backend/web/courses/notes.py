from uuid import UUID

from fastapi import File, UploadFile
from fastapi.routing import APIRouter

from backend.courses.models import CourseContentType
from backend.web.accounts.dependencies import EducatorDep
from backend.web.courses.dependencies import CourseNoteServiceDep

ID = UUID | str

router = APIRouter(prefix="/courses/notes", tags=["courses", "notes"])


@router.post("/{course_id}/notes")
async def upload_course_note(
    course_id: UUID,
    educator: EducatorDep,
    service: CourseNoteServiceDep,
    file: UploadFile = File(...),
):
    return await service.upload_course_note(
        course_id=course_id,
        educator=educator,
        upload=file,
        resource_type=CourseContentType.NOTES,
    )
