from typing import Protocol

from pytest import fixture
from sqlmodel import Session

from backend.accounts import User
from backend.courses.models import (
    Course,
    CourseCreate,
)
from backend.courses.repo.course_notes_repo import CourseNoteRepository
from backend.courses.repo.course_repo import CourseRepo
from backend.courses.service.course_access_service import CourseAccess
from backend.courses.service.course_note_service import CourseNoteService
from backend.courses.service.course_service import CourseService
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.storage import FileService


# @fixture
# def course_note_service(db_session: Session, storage):
#     return CourseNoteService(
#         db_session,
#         notes=CourseNoteRepository(db_session),
#         blocks=NoteBlockService,
#         access=CourseAccess(CourseRepo(db_session)),
#         files=FileService(storage, db_session),
#     )


@fixture
def course_service(
    db_session,
) -> CourseService:
    return CourseService(
        db_session,
    )


@fixture
def enrollment_service(db_session):
    return CourseEnrollmentService(db_session)


class MakeCourse(Protocol):
    async def __call__(self, educator: User, **overrides) -> Course: ...


@fixture
def make_course(course_service: CourseService) -> MakeCourse:
    async def make_course(educator: User, **overrides):
        default_course = {"name": "Mechanics101"}
        return await course_service.create(
            CourseCreate(**{**default_course, **overrides}), educator
        )

    return make_course
