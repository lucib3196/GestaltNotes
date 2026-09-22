from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from backend.core import logger
from backend.courses.service.access_code_service import CourseAccessCodeService
from backend.courses.service.course_service import CourseService
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.database import SessionDep


def get_course_service(session: SessionDep) -> CourseService:
    try:
        return CourseService(session)
    except Exception as e:
        logger.exception("Failed to initialize CourseService")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize course service",
        ) from e


def get_access_code_service(session: SessionDep) -> CourseAccessCodeService:
    try:
        return CourseAccessCodeService(session)
    except Exception as e:
        logger.exception("Failed to initialize CourseAccessCodeService")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize course access code service",
        ) from e


def get_enrollment_service(session: SessionDep) -> CourseEnrollmentService:
    try:
        return CourseEnrollmentService(session)
    except Exception as e:
        logger.exception("Failed to initialize CourseEnrollmentService")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize course enrollment service",
        ) from e


CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]
CourseAccessCodeServiceDep = Annotated[
    CourseAccessCodeService, Depends(get_access_code_service)
]
CourseEnrollmentServiceDep = Annotated[
    CourseEnrollmentService, Depends(get_enrollment_service)
]
