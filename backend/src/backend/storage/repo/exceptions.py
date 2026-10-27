class FileRepositoryError(Exception):
    """Base exception for file repository operations."""


class FileCreationError(FileRepositoryError):
    """Raised when file metadata creation fails."""


class FileRetrievalError(FileRepositoryError):
    """Raised when file metadata retrieval fails."""


class FileUpdateError(FileRepositoryError):
    """Raised when file metadata update fails."""


class FileDeletionError(FileRepositoryError):
    """Raised when file metadata deletion fails."""


class FileNotFoundError(FileRepositoryError, LookupError):
    """Raised when file metadata cannot be found."""

    def __init__(self, file_id: str) -> None:
        super().__init__(f"File '{file_id}' not found")
        self.file_id = file_id
