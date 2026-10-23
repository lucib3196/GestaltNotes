from uuid import UUID

from sqlmodel import Session, col, select

from backend.courses.models import CourseNote

from .exceptions import (
    LectureAlreadyProcessedError,
    LectureProcessingNoteNotFoundError,
    LectureProcessingRunNotFoundError,
)
from .models import LectureProcessingRun, ProcessingRun, ProcessingStatus
from .schema import LectureProcessingStatusRead, ProcessingRunRead


class LectureProcessingService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_successful_by_note(self, note_id: UUID) -> ProcessingRun | None:
        stmt = (
            select(ProcessingRun)
            .join(
                LectureProcessingRun,
                col(LectureProcessingRun.run_id) == ProcessingRun.id,
            )
            .where(
                LectureProcessingRun.note_id == note_id,
                ProcessingRun.status == ProcessingStatus.SUCCEEDED,
            )
        ).limit(1)
        return self._session.exec(stmt).first()

    def get_recent(self, note_id: UUID) -> ProcessingRun | None:
        stmt = (
            select(ProcessingRun)
            .join(
                LectureProcessingRun,
                col(LectureProcessingRun.run_id) == ProcessingRun.id,
            )
            .where(
                LectureProcessingRun.note_id == note_id,
            )
            .order_by(col(ProcessingRun.created_at).desc())
            .limit(1)
        )
        return self._session.exec(stmt).first()

    def get_processing_status(
        self,
        course_id: UUID,
        note_id: UUID,
    ) -> LectureProcessingStatusRead:
        self._get_note(course_id, note_id)

        has_succeeded = self.get_successful_by_note(note_id) is not None
        latest_run = self.get_recent(note_id)

        return LectureProcessingStatusRead(
            has_succeeded=has_succeeded,
            can_process=not has_succeeded,
            latest_run=(
                ProcessingRunRead.model_validate(latest_run)
                if latest_run is not None
                else None
            ),
        )

    def list_by_note(self, note_id: UUID) -> list[ProcessingRun]:
        """Return runs associated with a lecture note."""
        statement = (
            select(ProcessingRun)
            .join(
                LectureProcessingRun,
                col(LectureProcessingRun.run_id) == ProcessingRun.id,
            )
            .where(LectureProcessingRun.note_id == note_id)
        )
        return list(self._session.exec(statement).all())

    def _get_note(self, course_id: UUID, note_id: UUID) -> CourseNote:
        note = self._session.get(CourseNote, note_id)
        if note is None or note.course_id != course_id:
            raise LectureProcessingNoteNotFoundError("Course note not found")
        return note

    def assert_can_process(self, course_id: UUID, note_id: UUID) -> CourseNote:
        """Validate the association and reject notes with any successful run."""
        note = self._get_note(course_id, note_id)
        if self.get_successful_by_note(note_id) is not None:
            raise LectureAlreadyProcessedError(
                "This lecture has already been processed successfully."
            )
        return note

    def list_runs(self, course_id: UUID, note_id: UUID) -> list[ProcessingRun]:
        self._get_note(course_id, note_id)
        return self.list_by_note(note_id)

    def get_run(self, course_id: UUID, note_id: UUID, run_id: UUID) -> ProcessingRun:
        self._get_note(course_id, note_id)
        association = self._session.get(LectureProcessingRun, run_id)

        if association is None:
            raise LectureProcessingRunNotFoundError("Processing run not found")
        run = association.run
        return run
