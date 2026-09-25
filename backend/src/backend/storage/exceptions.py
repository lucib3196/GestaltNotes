from backend.storage.blob.exceptions import (
    BlobDirectoryNotFoundError,
    BlobNotFoundError,
    BlobStorageDeleteError,
    BlobStorageDirectoryError,
    BlobStorageError,
    BlobStorageMetadataError,
    BlobStorageReadError,
    BlobStorageUploadError,
    InvalidBlobKeyError,
)
from backend.storage.repo.exceptions import (
    FileCreationError,
    FileDeletionError,
    FileNotFoundError,
    FileRepositoryError,
    FileRetrievalError,
    FileUpdateError,
)


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


__all__ = [
    "BlobDirectoryNotFoundError",
    "BlobNotFoundError",
    "BlobStorageDeleteError",
    "BlobStorageDirectoryError",
    "BlobStorageError",
    "BlobStorageMetadataError",
    "BlobStorageReadError",
    "BlobStorageUploadError",
    "FileCreationError",
    "FileDeletionError",
    "FileNotFoundError",
    "FileRepositoryError",
    "FileRetrievalError",
    "FileServiceCreateError",
    "FileServiceDeletionError",
    "FileServiceError",
    "FileServiceRetrievalError",
    "FileServiceUpdateError",
    "FileUpdateError",
    "InvalidBlobKeyError",
]
