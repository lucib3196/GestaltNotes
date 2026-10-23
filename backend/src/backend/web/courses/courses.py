from uuid import UUID

from fastapi.routing import APIRouter
from starlette import status

from backend.courses.exceptions import CourseServiceException
from backend.courses.models import Course
from backend.courses.schema import CourseCreate, CourseDelete, CourseRead, CourseUpdate
from backend.web.accounts.dependencies import EducatorDep

from .dependencies import CourseServiceDep
from .http import course_http_exception

ID = UUID | str

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_service: CourseServiceDep,
    educator: EducatorDep,
    data: CourseCreate,
) -> Course:
    try:
        return await course_service.create_course(data, educator)
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


@router.get("/get_prof_courses", response_model=list[CourseRead])
async def get_prof_courses(
    course_service: CourseServiceDep,
    educator: EducatorDep,
) -> list[Course]:
    try:
        return await course_service.list_owned_courses(educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}", response_model=CourseRead)
async def get_course(
    course_service: CourseServiceDep,
    course_id: ID,
) -> Course:
    try:
        return await course_service.get_course(course_id)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.patch("/{course_id}", response_model=CourseRead)
async def update_course(
    course_service: CourseServiceDep,
    educator: EducatorDep,
    course_id: ID,
    data: CourseUpdate,
) -> Course:
    try:
        return await course_service.update_course(course_id, data, educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.delete("/{course_id}", response_model=CourseDelete)
async def delete_course(
    course_service: CourseServiceDep,
    educator: EducatorDep,
    course_id: ID,
) -> CourseDelete:
    try:
        return await course_service.delete_course(course_id, educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e
