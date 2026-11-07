from collections.abc import Callable
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from langchain_core.vectorstores import VectorStore
from starlette import status

from backend.core.exceptions import InvalidConfigError, MissingConfigError
from backend.courses.exceptions import CourseServiceException
from backend.courses.models import (
    Course,
    CourseEnrollment,
    CourseNote,
    CourseVectorStore,
    NoteBlock,
    NoteBlockUpdate,
)
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
from backend.courses.service.document_builder import NoteBlockDocumentBuilder
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.courses.service.note_block_service import NoteBlockService
from backend.courses.vector_store.course_vector_store_service import (
    CourseVectorStoreService,
)
from backend.database import SessionDep
from backend.indexer.indexer import IndexingService
from backend.web.accounts.dependencies import CurrentUserDep, EducatorDep
from backend.web.courses.http import course_http_exception
from backend.web.storage.dependency import FileServiceDep

# ---------------------------------------------------------------------------
# Basic repositories
# ---------------------------------------------------------------------------


def get_course_repo(session: SessionDep) -> CourseRepo:
    """Construct a repository using the request session; no authorization."""
    return CourseRepo(session)


CourseRepoDep = Annotated[CourseRepo, Depends(get_course_repo)]


def get_course_note_repo(session: SessionDep) -> CourseNoteRepository:
    """Construct a repository using the request session; no authorization."""
    return CourseNoteRepository(session)


CourseNoteRepoDep = Annotated[CourseNoteRepository, Depends(get_course_note_repo)]


def get_note_block_repo(session: SessionDep) -> NoteBlockRepo:
    """Construct a repository using the request session; no authorization."""
    return NoteBlockRepo(session)


NoteBlockRepoDep = Annotated[NoteBlockRepo, Depends(get_note_block_repo)]


def get_lecture_processing_repo(session: SessionDep) -> LectureProcessingRepository:
    """Construct a repository using the request session; no authorization."""
    return LectureProcessingRepository(session)


LectureProcessingRepoDep = Annotated[
    LectureProcessingRepository, Depends(get_lecture_processing_repo)
]


# ---------------------------------------------------------------------------
# Course service
# ---------------------------------------------------------------------------


def get_course_service(session: SessionDep) -> CourseService:
    """Build course operations using the request session."""
    return CourseService(session)


CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]

# ---------------------------------------------------------------------------
# Course access service
# ---------------------------------------------------------------------------


def get_course_access(repo: CourseRepoDep) -> CourseAccess:
    """Build owner checks using the shared course repository."""
    return CourseAccess(repo)


CourseAccessDep = Annotated[CourseAccess, Depends(get_course_access)]

# ---------------------------------------------------------------------------
# Enrollment service
# ---------------------------------------------------------------------------


def get_enrollment_service(session: SessionDep) -> CourseEnrollmentService:
    """Build enrollment operations using the request session."""
    return CourseEnrollmentService(session)


CourseEnrollmentServiceDep = Annotated[
    CourseEnrollmentService, Depends(get_enrollment_service)
]

# ---------------------------------------------------------------------------
# Course-note processing service
# ---------------------------------------------------------------------------


def get_course_note_processing_service(
    session: SessionDep,
) -> CourseNoteProcessingService:
    """Build database-only processing queries and eligibility checks."""
    return CourseNoteProcessingService(session)


CourseNoteProcessingServiceDep = Annotated[
    CourseNoteProcessingService, Depends(get_course_note_processing_service)
]

# ---------------------------------------------------------------------------
# Course and resource access checks
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


ReadableNoteBlockRepoDep = Annotated[NoteBlockRepo, Depends(get_note_block_repository)]


async def get_readable_note_block(
    block_id: UUID, course: ReadableCourseDep, blocks: ReadableNoteBlockRepoDep
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

# ---------------------------------------------------------------------------
# Course vector-store service
# ---------------------------------------------------------------------------


def get_course_vectorstore_service(session: SessionDep) -> CourseVectorStoreService:
    """Build configuration access without constructing a provider client."""
    return CourseVectorStoreService(session)


CourseVectorStoreServiceDep = Annotated[
    CourseVectorStoreService, Depends(get_course_vectorstore_service)
]

# ---------------------------------------------------------------------------
# Course vector-store configuration and client
# ---------------------------------------------------------------------------


def get_course_vectorstore_config(
    course: ReadableCourseDep,
    stores: CourseVectorStoreServiceDep,
) -> CourseVectorStore | None:
    """Return configuration for an authorized course without contacting a provider."""
    return stores.get_configuration(course.id)


CourseVectorStoreConfigDep = Annotated[
    CourseVectorStore | None, Depends(get_course_vectorstore_config)
]


def get_course_vectorstore(
    course: ReadableCourseDep,
    stores: CourseVectorStoreServiceDep,
) -> VectorStore:
    """Authorize course access before constructing its async vector-store client."""
    try:
        return stores.get_vectorstore(course.id, async_mode=True)
    except (InvalidConfigError, MissingConfigError, LookupError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="This course's indexing service is not available.",
        ) from exc


CourseVectorStoreDep = Annotated[VectorStore, Depends(get_course_vectorstore)]

# ---------------------------------------------------------------------------
# Note-block indexer
# ---------------------------------------------------------------------------


def get_indexer(
    vector_store: CourseVectorStoreDep,
    repo: NoteBlockRepoDep,
) -> IndexingService[NoteBlock, NoteBlockUpdate]:
    """Build an indexer targeting the requested course's vector store."""
    return IndexingService(
        repo=repo,
        vector_store=vector_store,
        builder=NoteBlockDocumentBuilder(),
    )


NoteBlockIndexerDep = Annotated[
    IndexingService[NoteBlock, NoteBlockUpdate], Depends(get_indexer)
]


def get_indexer_factory(
    course: ReadableCourseDep,
    stores: CourseVectorStoreServiceDep,
    repo: NoteBlockRepoDep,
) -> Callable[[], IndexingService[NoteBlock, NoteBlockUpdate]]:
    """Capture authorized course dependencies without constructing its store."""

    def build_indexer() -> IndexingService[NoteBlock, NoteBlockUpdate]:
        return get_indexer(get_course_vectorstore(course, stores), repo)

    return build_indexer


NoteBlockIndexerFactoryDep = Annotated[
    Callable[[], IndexingService[NoteBlock, NoteBlockUpdate]],
    Depends(get_indexer_factory),
]

# ---------------------------------------------------------------------------
# Note-block service
# ---------------------------------------------------------------------------


def get_note_block_service(
    session: SessionDep,
    repo: NoteBlockRepoDep,
    indexer_factory: NoteBlockIndexerFactoryDep,
) -> NoteBlockService:
    """Compose block operations without initializing the vector-store client."""
    return NoteBlockService(
        session=session, blocks=repo, indexer_factory=indexer_factory
    )


NoteBlockServiceDep = Annotated[NoteBlockService, Depends(get_note_block_service)]

# ---------------------------------------------------------------------------
# Course-note service
# ---------------------------------------------------------------------------


def get_course_note_service(
    session: SessionDep,
    file_service: FileServiceDep,
    notes: CourseNoteRepoDep,
    blocks: NoteBlockServiceDep,
    access: CourseAccessDep,
) -> CourseNoteService:
    """Compose note operations; initialize indexing only for block mutations."""
    return CourseNoteService(
        session=session,
        notes=notes,
        blocks=blocks,
        access=access,
        files=file_service,
    )


CourseNoteServiceDep = Annotated[CourseNoteService, Depends(get_course_note_service)]
