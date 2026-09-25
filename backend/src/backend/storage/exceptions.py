class BlobStorageError(Exception):
    """Base exception for blob storage operations."""


class BlobStorageUploadError(BlobStorageError):
    """Raised when uploading a blob fails."""


class BlobStorageReadError(BlobStorageError):
    """Raised when reading a blob fails."""


class BlobStorageDeleteError(BlobStorageError):
    """Raised when deleting a blob fails."""


class BlobStorageMetadataError(BlobStorageError):
    """Raised when retrieving blob metadata fails."""


class BlobStorageDirectoryError(BlobStorageError):
    """Raised when a directory-like prefix operation fails."""


class BlobNotFoundError(BlobStorageError, LookupError):
    """Raised when a blob cannot be found."""

    def __init__(self, key: str) -> None:
        super().__init__(f"Blob '{key}' not found")
        self.key = key


class BlobDirectoryNotFoundError(BlobStorageDirectoryError, LookupError):
    """Raised when a directory-like prefix cannot be found."""

    def __init__(self, key: str) -> None:
        super().__init__(f"Blob directory '{key}' not found")
        self.key = key


class InvalidBlobKeyError(BlobStorageError, ValueError):
    """Raised when a blob key cannot be normalized."""


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


class FileServiceError(Exception):
    """Base exception for file service operations."""


class FileServiceCreateError(FileServiceError):
    """Raised when file creation orchestration fails."""


class FileServiceRetrievalError(FileServiceError):
    """Raised when file retrieval orchestration fails."""


class FileServiceUpdateError(FileServiceError):
    """Raised when file update orchestration fails."""


class FileServiceDeletionError(FileServiceError):
    """Raised when file deletion orchestration fails."""
