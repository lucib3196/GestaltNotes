class UserServiceException(Exception):
    """Base exception for account service operations."""


class UserUpdateError(UserServiceException):
    """Exception when failed to update user."""


class UserNotFoundError(UserServiceException, LookupError):
    """Raised when a user cannot be found."""

    def __init__(self, user_id: str | None = None, message: str | None = None) -> None:
        detail = message or "User not found"
        if user_id:
            detail = f"User '{user_id}' not found"
        super().__init__(detail)
        self.user_id = user_id


class UserCreationError(UserServiceException):
    """Raised when user creation fails."""

class UserDeletionError(UserServiceException):
    """Raised when account deletion or rollback fails."""


class UserRoleLinkError(UserServiceException):
    """Raised when assigning a role to an account fails."""


class FirebaseAuthError(UserServiceException):
    """Raised when Firebase account operations fail."""


class AuthDrift(FirebaseAuthError):
    """Raised when database and Firebase user ids do not match."""