from uuid import UUID

from sqlmodel import Session, col, select

from backend.courses.notes.models import CourseNote
from backend.courses.notes.repo import CourseNoteRepository
from backend.courses.notes.schema import NoteOverview
from backend.processing.exceptions import (
    LectureAlreadyProcessedError,
    LectureProcessingRunNotFoundError,
)
from backend.processing.models import (
    LectureProcessingRun,
    ProcessingRun,
    ProcessingStatus,
)
from backend.processing.schema import LectureProcessingStatusRead, ProcessingRunRead


class CourseNoteProcessingService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._notes = CourseNoteRepository(session)

    async def get_note_overview(self, note_id: UUID) -> NoteOverview:
        note = await self._notes.get_note_read(note_id)
        summary = await self.get_processing_status(note_id)
        return NoteOverview(**note.model_dump(), processing=summary)

    async def list_notes_overview(self, course_id: UUID) -> list[NoteOverview]:
        notes = await self._notes.list_by_course(course_id)
        return [
            await self.get_note_overview(note.id)
            for note in notes
            if note.id is not None
        ]

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

    async def get_processing_status(
        self,
        note_id: UUID,
    ) -> LectureProcessingStatusRead:
        await self._notes.get_required(note_id)

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

    async def assert_can_process(self, note_id: UUID) -> CourseNote:
        """Reject notes with any successful processing run."""
        note = await self._notes.get_required(note_id)
        if self.get_successful_by_note(note_id) is not None:
            raise LectureAlreadyProcessedError(
                "This lecture has already been processed successfully."
            )
        return note

    async def list_runs(self, note_id: UUID) -> list[ProcessingRun]:
        await self._notes.get_required(note_id)
        return self.list_by_note(note_id)

    async def get_run(self, note_id: UUID, run_id: UUID) -> ProcessingRun:
        await self._notes.get_required(note_id)
        association = self._session.get(LectureProcessingRun, run_id)

        if association is None or association.note_id != note_id:
            raise LectureProcessingRunNotFoundError("Processing run not found")
        return association.run
