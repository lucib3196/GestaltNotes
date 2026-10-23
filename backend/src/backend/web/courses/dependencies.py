from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from starlette import status

from backend.core import logger
from backend.courses.models import Course, CourseEnrollment
from backend.courses.notes.course_note_service import CourseNoteService
from backend.courses.notes.models import CourseNote
from backend.courses.notes.note_block_service import NoteBlockService
from backend.courses.notes.processing_service import CourseNoteProcessingService
from backend.courses.notes.repo import CourseNoteRepository
from backend.courses.service.access_code_service import CourseAccessCodeService
from backend.courses.service.course_service import CourseService
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.database import SessionDep
from backend.web.accounts.dependencies import CurrentUserDep
from backend.web.storage.dependency import FileServiceDep


def get_note_block_service(session: SessionDep) -> NoteBlockService:
    return NoteBlockService(session)


def get_readable_course(
    course_id: UUID,
    session: SessionDep,
    user: CurrentUserDep,
) -> Course:
    course = session.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if user.id is not None and course.owner_id == user.id:
        return course
    enrollment = (
        session.get(CourseEnrollment, (user.id, course_id))
        if user.id is not None
        else None
    )
    if enrollment is None or not enrollment.active:
        raise HTTPException(status_code=403, detail="Course access denied")
    return course


NoteBlockServiceDep = Annotated[NoteBlockService, Depends(get_note_block_service)]
ReadableCourseDep = Annotated[Course, Depends(get_readable_course)]


async def get_readable_course_note(
    note_id: UUID,
    course: ReadableCourseDep,
    session: SessionDep,
) -> CourseNote:
    note = await CourseNoteRepository(session).get_by_course_and_note(
        course.id, note_id
    )
    if note is None:
        raise HTTPException(status_code=404, detail="Course note not found")
    return note


ReadableCourseNoteDep = Annotated[CourseNote, Depends(get_readable_course_note)]


def get_course_note_service(
    session: SessionDep,
    file_service: FileServiceDep,
) -> CourseNoteService:
    return CourseNoteService(file_service=file_service, session=session)


def get_course_service(session: SessionDep) -> CourseService:
    try:
        return CourseService(
            session,
        )
    except Exception as e:
        logger.exception("Failed to initialize CourseService")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize course service",
        ) from e


def get_access_code_service(session: SessionDep) -> CourseAccessCodeService:
    try:
        return CourseAccessCodeService(session)
    except Exception as e:
        logger.exception("Failed to initialize CourseAccessCodeService")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize course access code service",
        ) from e


def get_enrollment_service(
    session: SessionDep, course_service: "CourseServiceDep"
) -> CourseEnrollmentService:
    try:
        return CourseEnrollmentService(course_service, session)
    except Exception as e:
        logger.exception("Failed to initialize CourseEnrollmentService")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize course enrollment service",
        ) from e


def get_course_note_processing_service(
    session: SessionDep,
) -> CourseNoteProcessingService:
    return CourseNoteProcessingService(session)


CourseNoteServiceDep = Annotated[CourseNoteService, Depends(get_course_note_service)]
CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]

CourseAccessCodeServiceDep = Annotated[
    CourseAccessCodeService, Depends(get_access_code_service)
]
CourseEnrollmentServiceDep = Annotated[
    CourseEnrollmentService, Depends(get_enrollment_service)
]

CourseNoteProcessingServiceDep = Annotated[
    CourseNoteProcessingService,
    Depends(get_course_note_processing_service),
]
