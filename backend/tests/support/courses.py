from typing import Protocol

from pytest import fixture

from backend.accounts import User
from backend.courses import Course, CourseCreate
from backend.courses.service.course_note_service import CourseNoteService
from backend.courses.service.course_service import CourseService
from backend.courses.service.enrollment_service import CourseEnrollmentService


class FakeCourseNoteService:
    def course_prefix(self, course_id: str) -> str:
        return f"courses/{course_id}"


@fixture
def course_note_service(request, db_session) -> CourseNoteService:
    account_service_kind = getattr(
        getattr(request.node, "callspec", None),
        "params",
        {},
    ).get("account_service", "real")

    if account_service_kind == "fake":
        return FakeCourseNoteService()  # type: ignore[return-value]

    return CourseNoteService(db_session)


@fixture
def course_service(db_session, course_note_service: CourseNoteService) -> CourseService:
    return CourseService(db_session, course_note_service)


@fixture
def enrollment_service(course_service: CourseService, db_session):
    return CourseEnrollmentService(course_service, db_session)


class MakeCourse(Protocol):
    async def __call__(self, educator: User, **overrides) -> Course: ...


@fixture
def make_course(course_service: CourseService) -> MakeCourse:
    async def make_course(educator: User, **overrides):
        default_course = {"name": "Mechanics101"}
        return await course_service.create_course(
            CourseCreate(**{**default_course, **overrides}), educator
        )

    return make_course
