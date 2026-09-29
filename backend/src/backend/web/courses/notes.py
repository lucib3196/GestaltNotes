from uuid import UUID

from fastapi.routing import APIRouter

from backend.web.accounts.dependencies import EducatorDep

ID = UUID | str

router = APIRouter(prefix="/courses/notes", tags=["courses", "notes"])


@router.post("/{course_id}/notes")
async def upload_course_note(
    course_id: UUID,
    educator: EducatorDep,
    manager: CourseNoteManagerDep,
    file: UploadFile = File(...),
):
    return await manager.upload_course_note(
        course_id=course_id,
        educator=educator,
        upload=file,
        resource_type=CourseContentType.NOTES,
    )
