from datetime import datetime
from uuid import UUID

from fastapi.routing import APIRouter
from pydantic import BaseModel
from starlette import status

from backend.courses.exceptions import CourseServiceException
from backend.courses.models import CourseEnrollment
from backend.web.accounts.dependencies import EducatorDep, StudentDep

from .dependencies import CourseAccessCodeServiceDep
from .http import course_http_exception

ID = UUID | str

router = APIRouter(prefix="/courses", tags=["course-access-codes"])


class AccessCodeCreate(BaseModel):
    expires_at: datetime | None = None


class AccessCodeRead(BaseModel):
    code: str


class AccessCodeRedeem(BaseModel):
    code: str


@router.post(
    "/{course_id}/access-codes",
    response_model=AccessCodeRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_access_code(
    access_code_service: CourseAccessCodeServiceDep,
    educator: EducatorDep,
    course_id: ID,
    data: AccessCodeCreate,
) -> AccessCodeRead:
    try:
        code = await access_code_service.create_access_code(
            course_id,
            educator,
            expires_at=data.expires_at,
        )
        return AccessCodeRead(code=code)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.post("/{course_id}/access-codes/rotate", response_model=AccessCodeRead)
async def rotate_access_code(
    access_code_service: CourseAccessCodeServiceDep,
    educator: EducatorDep,
    course_id: ID,
    data: AccessCodeCreate,
) -> AccessCodeRead:
    try:
        code = await access_code_service.rotate_access_code(
            course_id,
            educator,
            expires_at=data.expires_at,
        )
        return AccessCodeRead(code=code)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.delete(
    "/{course_id}/access-codes/active",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def disable_active_access_codes(
    access_code_service: CourseAccessCodeServiceDep,
    educator: EducatorDep,
    course_id: ID,
) -> None:
    try:
        await access_code_service.disable_active_codes(course_id, educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.post(
    "/access-codes/redeem",
    response_model=CourseEnrollment,
    tags=["course-enrollments"],
)
async def redeem_access_code(
    access_code_service: CourseAccessCodeServiceDep,
    student: StudentDep,
    data: AccessCodeRedeem,
) -> CourseEnrollment:
    try:
        return await access_code_service.redeem_access_code(data.code, student)
    except CourseServiceException as e:
        raise course_http_exception(e) from e
