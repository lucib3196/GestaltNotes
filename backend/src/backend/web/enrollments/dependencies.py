from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from backend.core import logger
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.database import SessionDep
from backend.web.courses.dependencies import CourseServiceDep


def get_enrollment_service(
    session: SessionDep, course_service: "CourseServiceDep"
) -> CourseEnrollmentService:
    try:
        return CourseEnrollmentService(course_service, session)
    except Exception as e:
        logger.exception("Failed to initialize CourseEnrollmentService")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize course enrollment service",
        ) from e


CourseEnrollmentServiceDep = Annotated[
    CourseEnrollmentService, Depends(get_enrollment_service)
]
