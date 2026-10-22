from uuid import UUID

from pydantic import BaseModel, Field
from sqlmodel import Session, select

from .model import ProcessingRun, ProcessingStage, ProcessingStatus


class RunUpdate(BaseModel):
    celery_task_id: UUID | None = None
    task_type: str | None = None
    status: ProcessingStatus | None = None
    stage: ProcessingStage | None = None
    attempt_count: int | None = Field(default=None, ge=0)
    error_type: str | None = None
    error_message: str | None = None


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
