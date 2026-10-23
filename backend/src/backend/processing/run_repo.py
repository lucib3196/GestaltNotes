from uuid import UUID

from sqlmodel import Session, select

from .models import LectureProcessingRun, ProcessingRun, ProcessingStatus
from .schema import RunUpdate


class RunRepo:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, record: ProcessingRun) -> ProcessingRun:
        """Insert and flush a run without committing the transaction."""
        validated = ProcessingRun.model_validate(record.model_dump())

        self._session.add(validated)
        self._session.flush()
        self._session.refresh(validated)
        return validated

    def get(self, run_id: UUID) -> ProcessingRun | None:
        """Retrieve a processing run by its database ID."""
        return self._session.get(ProcessingRun, run_id)

    def get_by_celery_id(self, celery_task_id: UUID) -> ProcessingRun | None:
        """Retrieve a processing run by its Celery task ID."""
        statement = select(ProcessingRun).where(
            ProcessingRun.celery_task_id == celery_task_id
        )
        return self._session.exec(statement).one_or_none()

    def get_successful_by_note(self, note_id: UUID) -> ProcessingRun | None:
        """Find any successful run associated with a lecture note."""
        statement = (
            select(ProcessingRun)
            .join(LectureProcessingRun, LectureProcessingRun.run_id == ProcessingRun.id)
            .where(
                LectureProcessingRun.note_id == note_id,
                ProcessingRun.status == ProcessingStatus.SUCCEEDED,
            )
            .limit(1)
        )
        return self._session.exec(statement).first()

    def list_by_note(self, note_id: UUID) -> list[ProcessingRun]:
        """Return runs associated with a lecture note."""
        statement = (
            select(ProcessingRun)
            .join(LectureProcessingRun, LectureProcessingRun.run_id == ProcessingRun.id)
            .where(LectureProcessingRun.note_id == note_id)
        )
        return list(self._session.exec(statement).all())

    def update(
        self,
        record: ProcessingRun,
        changes: RunUpdate,
    ) -> ProcessingRun:
        """Update supplied fields without committing the transaction."""
        values = changes.model_dump(exclude_unset=True)

        # Validate the merged record before mutating the stored object.
        validated = ProcessingRun.model_validate(
            {
                **record.model_dump(),
                **values,
            }
        )

        for name in values:
            setattr(record, name, getattr(validated, name))

        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record
