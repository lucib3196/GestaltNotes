class LectureProcessingError(Exception):
    """Base error for lecture-processing operations."""


class LectureProcessingNoteNotFoundError(LectureProcessingError, LookupError):
    """The note does not exist in the requested course."""


class LectureProcessingRunNotFoundError(LectureProcessingError, LookupError):
    """The run does not exist for the requested note."""


class LectureAlreadyProcessedError(LectureProcessingError):
    """The note already has a successful processing run."""
