from uuid import UUID

from sqlmodel import Session

from backend.courses.models import CourseNote, NoteOverview
from backend.courses.repo.course_notes_repo import CourseNoteRepository
from backend.courses.repo.lecture_processing_repo import LectureProcessingRepository
from backend.processing.exceptions import (
    LectureAlreadyProcessedError,
    LectureProcessingInProgressError,
    LectureProcessingRunNotFoundError,
)
from backend.processing.models import (
    LectureProcessingStatusRead,
    ProcessingRun,
    ProcessingRunRead,
)


class CourseNoteProcessingService:
    """Build lecture-processing views and enforce processing eligibility."""

    def __init__(self, session: Session) -> None:
        self._notes = CourseNoteRepository(session)
        self._runs = LectureProcessingRepository(session)

    async def get_note_overview(self, note_id: UUID) -> NoteOverview:
        """Combine the resource's display data and current processing status."""
        note = await self._notes.get_note_read(note_id)
        processing = await self.get_processing_status(note_id)
        return NoteOverview(**note.model_dump(), processing=processing)

    async def list_notes_overview(self, course_id: UUID) -> list[NoteOverview]:
        """Return processing overviews for notes belonging to this course."""
        notes = await self._notes.list_by_course(course_id)
        return [await self.get_note_overview(note.id) for note in notes]

    async def get_processing_status(self, note_id: UUID) -> LectureProcessingStatusRead:
        """Report historical success, latest activity, and eligibility."""
        await self._notes.get_required(note_id)
        has_succeeded = self._runs.get_latest_successful(note_id) is not None
        active = self._runs.get_latest_active(note_id)
        latest = self._runs.get_latest(note_id)
        return LectureProcessingStatusRead(
            has_succeeded=has_succeeded,
            can_process=not has_succeeded and active is None,
            latest_run=(
                ProcessingRunRead.model_validate(latest) if latest is not None else None
            ),
        )

    async def assert_can_process(self, note_id: UUID) -> CourseNote:
        """Reject notes with a successful or currently active processing run."""
        note = await self._notes.get_required(note_id)
        if self._runs.get_latest_successful(note_id) is not None:
            raise LectureAlreadyProcessedError(
                "This lecture has already been processed successfully."
            )
        if self._runs.get_latest_active(note_id) is not None:
            raise LectureProcessingInProgressError(
                "This lecture is already queued or being processed."
            )
        return note

    async def list_runs(self, note_id: UUID) -> list[ProcessingRun]:
        """List this note's runs, newest first, after verifying the note exists."""
        await self._notes.get_required(note_id)
        return list(self._runs.list_by_note(note_id))

    async def get_run(self, note_id: UUID, run_id: UUID) -> ProcessingRun:
        """Retrieve a run only within the requested note."""
        await self._notes.get_required(note_id)
        run = self._runs.get_by_note_and_run(note_id, run_id)
        if run is None:
            raise LectureProcessingRunNotFoundError(
                f"Processing run '{run_id}' not found for note '{note_id}'"
            )
        return run
