from fastapi import HTTPException
from starlette import status

from backend.courses.exceptions import (
    CourseAccessCodeDisabledError,
    CourseAccessCodeExpiredError,
    CourseAccessCodeInvalidError,
    CourseAccessCodeNotFoundError,
    CourseEnrollmentAlreadyExistsError,
    CourseEnrollmentNotFoundError,
    CourseEnrollmentPermissionError,
    CourseNotFoundError,
    CourseOwnershipError,
    CoursePermissionError,
    CourseServiceException,
)


def course_http_exception(error: Exception) -> HTTPException:
    if isinstance(error, (CourseNotFoundError, CourseAccessCodeNotFoundError)):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    if isinstance(error, CourseEnrollmentAlreadyExistsError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))

    if isinstance(
        error,
        (
            CourseOwnershipError,
            CoursePermissionError,
            CourseEnrollmentPermissionError,
            CourseAccessCodeDisabledError,
            CourseAccessCodeExpiredError,
            CourseAccessCodeInvalidError,
        ),
    ):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))

    if isinstance(error, CourseEnrollmentNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    if isinstance(error, CourseServiceException):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Course operation failed",
    )
