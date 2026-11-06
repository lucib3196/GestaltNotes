from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from starlette import status

from backend.core.exceptions import InvalidConfigError, MissingConfigError
from backend.courses.exceptions import CourseServiceException
from backend.courses.models import Course, CourseEnrollment, CourseNote, NoteBlock
from backend.courses.repo.course_notes_repo import CourseNoteRepository
from backend.courses.repo.course_repo import CourseRepo
from backend.courses.repo.lecture_processing_repo import LectureProcessingRepository
from backend.courses.repo.note_blocks_repo import NoteBlockRepo
from backend.courses.service.course_access_service import CourseAccess
from backend.courses.service.course_note_processing_service import (
    CourseNoteProcessingService,
)
from backend.courses.service.course_note_service import CourseNoteService
from backend.courses.service.course_service import CourseService
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.courses.service.note_block_service import NoteBlockService
from backend.courses.vector_store.course_vector_store_service import (
    CourseVectorStoreService,
)
from backend.database import SessionDep
from backend.web.accounts.dependencies import CurrentUserDep, EducatorDep
from backend.web.courses.http import course_http_exception
from backend.web.storage.dependency import FileServiceDep

# ---------------------------------------------------------------------------
# Service construction
# ---------------------------------------------------------------------------


def get_course_service(session: SessionDep) -> CourseService:
    """Build course operations using the request's database session."""
    return CourseService(session)


CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]


def get_course_note_service(
    session: SessionDep,
    file_service: FileServiceDep,
) -> CourseNoteService:
    """Build note operations using one shared database session."""
    return CourseNoteService(
        session=session,
        notes=CourseNoteRepository(session),
        blocks=NoteBlockRepo(session),
        runs=LectureProcessingRepository(session),
        access=CourseAccess(CourseRepo(session)),
        files=file_service,
        stores=CourseVectorStoreService(session),
    )


CourseNoteServiceDep = Annotated[CourseNoteService, Depends(get_course_note_service)]


def get_course_note_processing_service(
    session: SessionDep,
) -> CourseNoteProcessingService:
    """Build lecture-run queries and processing eligibility checks."""
    return CourseNoteProcessingService(session)


CourseNoteProcessingServiceDep = Annotated[
    CourseNoteProcessingService,
    Depends(get_course_note_processing_service),
]


def get_enrollment_service(session: SessionDep) -> CourseEnrollmentService:
    """Build enrollment operations using the request's database session."""
    return CourseEnrollmentService(session)


CourseEnrollmentServiceDep = Annotated[
    CourseEnrollmentService, Depends(get_enrollment_service)
]


# ---------------------------------------------------------------------------
# Read access: courses and course notes
# ---------------------------------------------------------------------------


def get_readable_course(
    course_id: UUID,
    session: SessionDep,
    user: CurrentUserDep,
) -> Course:
    """Allow the course owner or an actively enrolled user to read the course."""
    course = session.get(Course, course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )
    if user.id is not None and course.owner_id == user.id:
        return course
    enrollment = (
        session.get(CourseEnrollment, (user.id, course_id))
        if user.id is not None
        else None
    )
    if enrollment is None or not enrollment.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Course access denied"
        )
    return course


ReadableCourseDep = Annotated[Course, Depends(get_readable_course)]


async def get_readable_course_note(
    note_id: UUID,
    course: ReadableCourseDep,
    session: SessionDep,
) -> CourseNote:
    """Resolve the note within a course the caller is allowed to read."""
    note = await CourseNoteRepository(session).get_by_course_and_note(
        course.id, note_id
    )
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course note not found"
        )
    return note


ReadableCourseNoteDep = Annotated[CourseNote, Depends(get_readable_course_note)]


# ---------------------------------------------------------------------------
# Owner access: courses and course notes
# ---------------------------------------------------------------------------


async def get_owned_course(
    course_id: UUID,
    session: SessionDep,
    user: EducatorDep,
) -> Course:
    """Require an educator who owns the requested course."""
    try:
        return await CourseAccess(CourseRepo(session)).require_owner(course_id, user)
    except CourseServiceException as exc:
        raise course_http_exception(exc) from exc


OwnedCourseDep = Annotated[Course, Depends(get_owned_course)]


async def get_owned_course_note(
    note_id: UUID,
    course: OwnedCourseDep,
    session: SessionDep,
) -> CourseNote:
    """Resolve a note within a course owned by the educator."""
    note = await CourseNoteRepository(session).get_by_course_and_note(
        course.id, note_id
    )
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course note not found"
        )
    return note


OwnedCourseNoteDep = Annotated[CourseNote, Depends(get_owned_course_note)]


# ---------------------------------------------------------------------------
# Scoped block reads and owner-only indexing operations
# ---------------------------------------------------------------------------


def get_note_block_repository(
    _course: ReadableCourseDep, session: SessionDep
) -> NoteBlockRepo:
    """Authorize reads before constructing a database-only repository."""
    return NoteBlockRepo(session)


NoteBlockRepoDep = Annotated[NoteBlockRepo, Depends(get_note_block_repository)]


async def get_readable_note_block(
    block_id: UUID, course: ReadableCourseDep, blocks: NoteBlockRepoDep
) -> NoteBlock:
    """Resolve a block within a readable course without accessing embeddings."""
    block = await blocks.get(block_id)
    if (
        block is None
        or block.course_note is None
        or block.course_note.course_id != course.id
    ):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Note block not found")
    return block


ReadableNoteBlockDep = Annotated[NoteBlock, Depends(get_readable_note_block)]


async def get_owned_note_block(
    block_id: UUID, course: OwnedCourseDep, session: SessionDep
) -> NoteBlock:
    """Scope mutations to an owned course and reject active note processing."""
    block = await NoteBlockRepo(session).get(block_id)
    if (
        block is None
        or block.course_note is None
        or block.course_note.course_id != course.id
    ):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Note block not found")
    if (
        LectureProcessingRepository(session).get_latest_active(block.course_note_id)
        is not None
    ):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Wait for this note's processing to finish before changing its blocks.",
        )
    return block


OwnedNoteBlockDep = Annotated[NoteBlock, Depends(get_owned_note_block)]


def get_note_block_service(
    block: OwnedNoteBlockDep, session: SessionDep
) -> NoteBlockService:
    """Construct indexing only after ownership, scope, and activity checks."""
    try:
        return NoteBlockService.from_dependencies(session, block.course_note.course_id)
    except (InvalidConfigError, MissingConfigError, LookupError, ValueError) as exc:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "This course's indexing service is not available.",
        ) from exc


NoteBlockServiceDep = Annotated[NoteBlockService, Depends(get_note_block_service)]
