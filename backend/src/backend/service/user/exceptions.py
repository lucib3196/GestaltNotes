from backend.accounts.exceptions import (
    UserServiceException,
)


class UserValidationError(UserServiceException, ValueError):
    """Raised when user input fails validation."""


class UserAlreadyExistsError(UserServiceException):
    """Raised when attempting to create a user that already exists."""


class UserRoleLinkError(UserServiceException):
    """Raised when role to user failes"""


class UserDeletionError(UserServiceException):
    """Raised when user deletion fails."""


class UserRoleNotFoundError(UserServiceException):
    """Raised when a requested role does not exist."""


class UserRoleAssignmentError(UserServiceException):
    """Raised when role assignment to a user fails."""


class UserInstitutionNotFoundError(UserServiceException):
    """Raised when an institution is invalid or missing."""


class UserInstitutionAssignmentError(UserServiceException):
    """Raised when assigning a user institution fails."""


class UserReadError(UserServiceException):
    """Raised when user data cannot be read."""


class FirebaseAuthError(UserServiceException):
    """base exception for fb related auth"""


class AuthDrift(FirebaseAuthError):
    """base exception for fb related auth"""


class DeveloperAccessDeniedError(UserServiceException, PermissionError):
    """Raised when a user is not allowed to perform a developer action."""

    def __init__(
        self,
        reason: str,
        user_id: str | None = None,
        question_id: str | None = None,
    ) -> None:
        message = "Developer access denied"
        if user_id:
            message += f" for user {user_id}"
        if question_id:
            message += f" on question {question_id}"
        if reason:
            message += f": {reason}"
        super().__init__(message)
        self.user_id = user_id
        self.question_id = question_id
        self.reason = reason


class DeveloperProfileError(UserServiceException):
    """Raised when developer profile data cannot be retrieved or prepared."""

    def __init__(self, action: str, user_id: str, details: str = "") -> None:
        message = f"Failed to {action} developer profile for user {user_id}"
        if details:
            message += f": {details}"
        super().__init__(message)
        self.action = action
        self.user_id = user_id
        self.details = details


class DeveloperProfileNotSetError(DeveloperProfileError):
    """Raised when developer profile has not been configured for a user."""


# Backwards-compatible aliases for existing imports/usages.
DeveloperAccessDenied = DeveloperAccessDeniedError
DeveloperProfileNotSet = DeveloperProfileNotSetError
