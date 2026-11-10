from collections.abc import Sequence
from typing import Literal
from uuid import UUID

from sqlmodel import Session, col, select

from backend.adapters import Repository
from backend.processing.models import (
    LectureProcessingRun,
    ProcessingRun,
    ProcessingStatus,
    ProcessingUpdate,
)


class LectureProcessingRepository(Repository[ProcessingRun, ProcessingUpdate]):
    """Query processing runs within their associated course notes."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, ProcessingRun)

    def get_by_note_and_run(self, note_id: UUID, run_id: UUID) -> ProcessingRun | None:
        """Return the run only if it belongs to the requested note."""
        stmt = (
            select(ProcessingRun)
            .join(
                LectureProcessingRun,
                col(LectureProcessingRun.run_id) == ProcessingRun.id,
            )
            .where(
                LectureProcessingRun.note_id == note_id,
                ProcessingRun.id == run_id,
            )
        )
        return self._session.exec(stmt).one_or_none()

    def list_by_note(
        self,
        note_id: UUID,
        *,
        order: Literal["newest", "oldest"] = "newest",
        limit: int | None = None,
        statuses: Sequence[ProcessingStatus] | None = None,
    ) -> Sequence[ProcessingRun]:
        """Filter before ordering and limiting; an empty status list matches nothing."""
        if limit is not None and limit < 1:
            raise ValueError("Limit must be at least 1")

        stmt = (
            select(ProcessingRun)
            .join(
                LectureProcessingRun,
                col(LectureProcessingRun.run_id) == ProcessingRun.id,
            )
            .where(LectureProcessingRun.note_id == note_id)
        )
        if statuses is not None:
            stmt = stmt.where(col(ProcessingRun.status).in_(statuses))

        if order == "newest":
            stmt = stmt.order_by(
                col(ProcessingRun.created_at).desc(),
                col(ProcessingRun.id).desc(),
            )
        elif order == "oldest":
            stmt = stmt.order_by(
                col(ProcessingRun.created_at).asc(),
                col(ProcessingRun.id).asc(),
            )
        else:
            raise ValueError(f"Unsupported order: {order}")

        if limit is not None:
            stmt = stmt.limit(limit)
        return self._session.exec(stmt).all()

    def get_latest(self, note_id: UUID) -> ProcessingRun | None:
        """Return the most recently created run for the note."""
        runs = self.list_by_note(note_id, limit=1)
        return runs[0] if runs else None

    def get_latest_successful(self, note_id: UUID) -> ProcessingRun | None:
        """Return the newest successful run, even if a later run failed."""
        runs = self.list_by_note(note_id, statuses=[ProcessingStatus.SUCCESS], limit=1)
        return runs[0] if runs else None

    def get_latest_active(self, note_id: UUID) -> ProcessingRun | None:
        """Return the newest pending, running, or retrying run for the note."""
        runs = self.list_by_note(
            note_id,
            statuses=[
                ProcessingStatus.PENDING,
                ProcessingStatus.RECEIVED,
                ProcessingStatus.STARTED,
                ProcessingStatus.PROGRESS,
                ProcessingStatus.RETRY,
            ],
            limit=1,
        )
        return runs[0] if runs else None
