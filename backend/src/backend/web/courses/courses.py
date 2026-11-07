from uuid import UUID

from fastapi.routing import APIRouter
from starlette import status

from backend.courses.exceptions import CourseServiceException
from backend.courses.models import (
    Course,
    CourseCreate,
    CourseDelete,
    CourseRead,
    CourseUpdate,
)
from backend.web.accounts.dependencies import EducatorDep

from .dependencies import CourseServiceDep, ReadableCourseDep
from .http import course_http_exception

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_service: CourseServiceDep,
    educator: EducatorDep,
    data: CourseCreate,
) -> Course:
    try:
        return await course_service.create(data, educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/", response_model=list[CourseRead])
async def list_owned_courses(
    course_service: CourseServiceDep,
    educator: EducatorDep,
) -> list[Course]:
    try:
        return await course_service.list_owned_courses(educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}", response_model=CourseRead)
async def get_course(course: ReadableCourseDep) -> Course:
    return course


@router.patch("/{course_id}", response_model=CourseRead)
async def update_course(
    course_service: CourseServiceDep,
    educator: EducatorDep,
    course_id: UUID,
    data: CourseUpdate,
) -> Course:
    try:
        return await course_service.update(course_id, data, educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.delete("/{course_id}", response_model=CourseDelete)
async def delete_course(
    course_service: CourseServiceDep,
    educator: EducatorDep,
    course_id: UUID,
) -> CourseDelete:
    try:
        return await course_service.delete(course_id, educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e
