from typing import Protocol

from pytest import fixture

from backend.accounts import User
from backend.courses.models import Course, CourseCreate
from backend.courses.notes.course_note_service import CourseNoteService
from backend.courses.service.course_service import CourseService
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.storage import FileService


class FakeCourseNoteService:
    def course_prefix(self, course_id: str) -> str:
        return f"courses/{course_id}"


@fixture
def course_note_service(request, db_session, storage) -> CourseNoteService:
    account_service_kind = getattr(
        getattr(request.node, "callspec", None),
        "params",
        {},
    ).get("account_service", "real")

    if account_service_kind == "fake":
        return FakeCourseNoteService()  # type: ignore[return-value]

    return CourseNoteService(db_session, FileService(storage, db_session))


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
