import pytest
from pytest import fixture
from backend.courses.service.storage_service import CourseStorageService
from backend.core.settings import get_settings
from backend.courses.service.course_service import CourseService

settings = get_settings()


@fixture
def course_storage() -> CourseStorageService:
    return CourseStorageService(settings.STORAGE_BUCKET)  # type: ignore


@fixture
def course_service(db_session, course_storage: CourseStorageService) -> CourseService:
    return CourseService(db_session, course_storage)
