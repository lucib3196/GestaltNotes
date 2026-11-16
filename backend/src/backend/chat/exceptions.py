class ThreadBaseException(Exception):
    """Base exception for thread base operations"""


class ThreadNotFound(ThreadBaseException):
    """Base exceptions when thread is not found"""


class ThreadCreateError(ThreadBaseException):
    """Exceptions when thread creation fails"""


class ThreadRetrievalError(ThreadBaseException):
    """Exception when failure to get thread"""


class ThreadUpdateError(ThreadBaseException):
    """Exception when failure to update thread"""


class ThreadMessageRetrievalError(ThreadBaseException):
    """Failed to retrieve messages from LangGraph."""


class ThreadDeleteError(ThreadBaseException):
    """SQL thread deletion failed."""


class ThreadClientDeleteError(ThreadBaseException):
    """Remote deletion failed; SQL deletion was rolled back."""


class ThreadDeleteCommitError(ThreadDeleteError):
    """Remote deletion succeeded, but the SQL commit failed."""


class PromptServiceError(Exception):
    """A prompt persistence operation failed."""


class PromptNotFoundError(PromptServiceError, LookupError):
    """The requested prompt does not exist."""
