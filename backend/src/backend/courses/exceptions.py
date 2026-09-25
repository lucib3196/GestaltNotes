class CourseServiceException(Exception):
    """Base exception for course service operations."""


class CourseCreationError(CourseServiceException):
    """Raised when course creation fails."""


class CourseUpdateError(CourseServiceException):
    """Raised when course update fails."""


class CourseDeletionError(CourseServiceException):
    """Raised when course deletion fails."""


class CourseRetrievalError(CourseServiceException):
    """Raised when course retrieval fails."""


class CourseNotFoundError(CourseServiceException, LookupError):
    """Raised when a course cannot be found."""

    def __init__(self, course_id: str | None = None) -> None:
        detail = "Course not found"
        if course_id:
            detail = f"Course '{course_id}' not found"
        super().__init__(detail)
        self.course_id = course_id


class CourseOwnershipError(CourseServiceException, PermissionError):
    """Raised when a user does not own the course."""


class CoursePermissionError(CourseServiceException, PermissionError):
    """Raised when a user cannot perform a course action."""


class CourseNoteServiceError(CourseServiceException):
    """Base exception for course note operations."""


class CourseNoteAssociationError(CourseNoteServiceError):
    """Raised when associating a file with a course fails."""


class CourseNoteRetrievalError(CourseNoteServiceError):
    """Raised when retrieving course notes fails."""


class CourseNoteNotFoundError(CourseNoteServiceError, LookupError):
    """Raised when a course note association cannot be found."""

    def __init__(self, course_id: str, file_id: str) -> None:
        super().__init__(f"File '{file_id}' is not attached to course '{course_id}'")
        self.course_id = course_id
        self.file_id = file_id


class CourseAccessCodeError(CourseServiceException):
    """Base exception for course access code operations."""


class CourseAccessCodeCreationError(CourseAccessCodeError):
    """Raised when access code creation fails."""


class CourseAccessCodeRetrievalError(CourseAccessCodeError):
    """Raised when access code retrieval fails."""


class CourseAccessCodeNotFoundError(CourseAccessCodeError, LookupError):
    """Raised when an access code cannot be found."""


class CourseAccessCodeInvalidError(CourseAccessCodeError, PermissionError):
    """Raised when an access code is invalid."""


class CourseAccessCodeExpiredError(CourseAccessCodeError, PermissionError):
    """Raised when an access code is expired."""


class CourseAccessCodeDisabledError(CourseAccessCodeError, PermissionError):
    """Raised when an access code is disabled."""


class CourseEnrollmentError(CourseAccessCodeError):
    """Raised when redeeming an access code cannot enroll a student."""


class CourseEnrollmentServiceError(CourseServiceException):
    """Base exception for course enrollment operations."""


class CourseEnrollmentCreationError(CourseEnrollmentServiceError):
    """Raised when enrollment creation fails."""


class CourseEnrollmentDeletionError(CourseEnrollmentServiceError):
    """Raised when enrollment deletion fails."""


class CourseEnrollmentRetrievalError(CourseEnrollmentServiceError):
    """Raised when enrollment retrieval fails."""


class CourseEnrollmentNotFoundError(CourseEnrollmentServiceError, LookupError):
    """Raised when an enrollment cannot be found."""


class CourseEnrollmentAlreadyExistsError(CourseEnrollmentServiceError):
    """Raised when a student is already enrolled in a course."""


class CourseEnrollmentPermissionError(CourseEnrollmentServiceError, PermissionError):
    """Raised when a user cannot perform an enrollment action."""
