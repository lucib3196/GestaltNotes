class GeneratedContentServiceError(Exception):
    """Base exception for generated content service operations."""


class GeneratedContentValidationError(GeneratedContentServiceError, ValueError):
    """Raised when generated MCQ payload validation fails."""


class UnsupportedSchemaVersionError(GeneratedContentValidationError):
    """Raised when a schema version is not supported."""

    def __init__(self, schema_version: int) -> None:
        super().__init__(
            f"Unsupported schema version '{schema_version}'. "
            "Only schema version 1 is currently supported."
        )
        self.schema_version = schema_version


class GeneratedContentPersistenceError(GeneratedContentServiceError):
    """Raised when saving generated content fails."""


class GeneratedContentBatchSaveError(GeneratedContentServiceError):
    """Raised when batch saving generated content fails."""


class GeneratedContentRetrievalError(GeneratedContentServiceError):
    """Raised when retrieval of generated MCQs fails."""


class GeneratedContentNotFoundError(GeneratedContentServiceError, LookupError):
    """Raised when a generated MCQ cannot be found."""

    def __init__(self, quiz_id: str | None = None) -> None:
        message = "Generated MCQ not found"
        if quiz_id:
            message = f"Generated MCQ '{quiz_id}' not found"
        super().__init__(message)
        self.quiz_id = quiz_id


class GeneratedContentDeletionError(GeneratedContentServiceError):
    """Raised when deletion of generated MCQs fails."""
