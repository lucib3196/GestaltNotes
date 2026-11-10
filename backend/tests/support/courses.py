from typing import Protocol

from pytest import fixture

from backend.accounts import User
from backend.courses.models import (
    Course,
    CourseCreate,
)
from backend.courses.service.course_management import CourseManagementService
from backend.courses.service.enrollment_service import CourseEnrollmentService

# @fixture
# def course_note_service(db_session: Session, storage):
#     return CourseNoteService(
#         db_session,
#         notes=CourseNoteRepository(db_session),
#         blocks=NoteBlockService,
#         access=CourseManagementService(CourseRepo(db_session)),
#         files=FileService(storage, db_session),
#     )


@fixture
def course_service(
    db_session,
) -> CourseManagementService:
    return CourseManagementService(
        db_session,
    )


@fixture
def enrollment_service(db_session):
    return CourseEnrollmentService(db_session)


class MakeCourse(Protocol):
    async def __call__(self, educator: User, **overrides) -> Course: ...


@fixture
def make_course(course_service: CourseManagementService) -> MakeCourse:
    async def make_course(educator: User, **overrides):
        default_course = {"name": "Mechanics101"}
        return await course_service.create(
            CourseCreate(**{**default_course, **overrides}), educator
        )

    return make_course
