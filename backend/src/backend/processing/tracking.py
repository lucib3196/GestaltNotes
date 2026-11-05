from collections.abc import Generator
from contextlib import contextmanager
from time import perf_counter
from uuid import UUID

from celery import Task
from celery.exceptions import Ignore, Reject, Retry

from backend.core.logger import logger
from backend.database.config import open_session

from .models import ProcessingStage, ProcessingStatus, ProcessingUpdate
from .processing_run_repository import ProcessingRunRepository


def update_run(run_id: UUID, changes: ProcessingUpdate) -> None:
    """Persist a run update in its own transaction."""
    with open_session() as session, session.begin():
        repo = ProcessingRunRepository(session)
        run = repo.get(run_id)
        if run is None:
            raise LookupError(f"Processing run '{run_id}' not found")
        repo.update(run, changes)


def try_update_run(run_id: UUID, changes: ProcessingUpdate) -> None:
    """Record an exceptional outcome without replacing the original error."""
    try:
        update_run(run_id, changes)
    except Exception:
        logger.exception(
            "Could not persist processing status: run_id=%s status=%s",
            run_id,
            changes.status,
        )


@contextmanager
def processing_state(
    *,
    task: Task,
    run_id: UUID,
    stage: ProcessingStage,
    final_stage: bool = False,
) -> Generator[None]:
    """Track a stage, preserving exceptions raised by the processing work."""
    task_id = task.request.id
    started = perf_counter()

    # Required: don't start work if its run cannot be updated.
    update_run(
        run_id,
        ProcessingUpdate(
            status=ProcessingStatus.STARTED,
            stage=stage,
            error_type=None,
            error_message=None,
        ),
    )

    logger.info(
        "Processing stage started: run_id=%s task_id=%s stage=%s",
        run_id,
        task_id,
        stage.value,
    )

    try:
        task.update_state(
            state=ProcessingStatus.PROGRESS.value,
            meta={"run_id": str(run_id), "stage": stage.value},
        )
        yield

        if final_stage:
            update_run(run_id, ProcessingUpdate(status=ProcessingStatus.SUCCESS))

    except Retry:
        try_update_run(
            run_id,
            ProcessingUpdate(status=ProcessingStatus.RETRY, stage=stage),
        )
        logger.warning(
            "Processing retry requested: run_id=%s stage=%s", run_id, stage.value
        )
        raise

    except (Ignore, Reject):
        # These are Celery control signals, not ordinary processing failures.
        raise

    except Exception as exc:
        logger.exception(
            "Processing stage failed: run_id=%s task_id=%s stage=%s",
            run_id,
            task_id,
            stage.value,
        )
        try_update_run(
            run_id,
            ProcessingUpdate(
                status=ProcessingStatus.FAILURE,
                stage=stage,
                error_type=type(exc).__name__,
                error_message=f"Processing failed during {stage.value}",
            ),
        )
        raise

    else:
        logger.info(
            "Processing stage completed: run_id=%s stage=%s elapsed_seconds=%.2f",
            run_id,
            stage.value,
            perf_counter() - started,
        )
