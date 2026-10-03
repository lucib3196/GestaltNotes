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
