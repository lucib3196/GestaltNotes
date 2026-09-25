import pytest
from pytest import fixture
from backend.courses.service.storage_service import CourseStorageService
from backend.core.settings import get_settings
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.courses.service.course_service import CourseService
from backend.courses import Course, CourseCreate
from typing import Protocol
from backend.accounts import User

settings = get_settings()


class FakeCourseStorageService:
    def course_prefix(self, course_id: str) -> str:
        return f"courses/{course_id}"


@fixture
def course_storage(request) -> CourseStorageService:
    account_service_kind = getattr(
        getattr(request.node, "callspec", None),
        "params",
        {},
    ).get("account_service", "real")

    if account_service_kind == "fake":
        return FakeCourseStorageService()  # type: ignore[return-value]

    request.getfixturevalue("firebase_app_for_tests")
    return CourseStorageService(settings.STORAGE_BUCKET)  # type: ignore[arg-type]


@fixture
def course_service(db_session, course_storage: CourseStorageService) -> CourseService:
    return CourseService(db_session, course_storage)


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
