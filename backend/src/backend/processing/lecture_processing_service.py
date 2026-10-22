from uuid import UUID

from sqlmodel import Session

from backend.courses.models import CourseNote

from .exceptions import (
    LectureAlreadyProcessedError,
    LectureProcessingNoteNotFoundError,
    LectureProcessingRunNotFoundError,
)
from .models import LectureProcessingRun, ProcessingRun
from .run_repo import RunRepo


class LectureProcessingService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._runs = RunRepo(session)

    def _get_note(self, course_id: UUID, note_id: UUID) -> CourseNote:
        note = self._session.get(CourseNote, note_id)
        if note is None or note.course_id != course_id:
            raise LectureProcessingNoteNotFoundError("Course note not found")
        return note

    def assert_can_process(self, course_id: UUID, note_id: UUID) -> CourseNote:
        """Validate the association and reject notes with any successful run."""
        note = self._get_note(course_id, note_id)
        if self._runs.get_successful_by_note(note_id) is not None:
            raise LectureAlreadyProcessedError(
                "This lecture has already been processed successfully."
            )
        return note

    def list_runs(self, course_id: UUID, note_id: UUID) -> list[ProcessingRun]:
        self._get_note(course_id, note_id)
        return self._runs.list_by_note(note_id)

    def get_run(self, course_id: UUID, note_id: UUID, run_id: UUID) -> ProcessingRun:
        self._get_note(course_id, note_id)
        association = self._session.get(LectureProcessingRun, run_id)
        if association is None or association.note_id != note_id:
            raise LectureProcessingRunNotFoundError("Processing run not found")
        run = self._runs.get(run_id)
        if run is None:
            raise LectureProcessingRunNotFoundError("Processing run not found")
        return run
