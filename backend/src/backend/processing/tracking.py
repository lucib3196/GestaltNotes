from collections.abc import Generator
from contextlib import contextmanager
from time import perf_counter
from uuid import UUID

from celery.exceptions import Ignore, Reject, Retry

from backend.core.logger import logger
from backend.database.config import open_session

from .models import ProcessingStage, ProcessingStatus
from .run_repo import RunRepo
from .schema import RunUpdate


@contextmanager
def processing_update(
    run_id: UUID,
    *,
    task_id: UUID,
    stage: ProcessingStage,
    final_stage: bool = False,
) -> Generator[None]:
    """Persist stage lifecycle updates around work on an existing run."""
    started = perf_counter()

    def update_run(changes: RunUpdate) -> None:
        with open_session() as session, session.begin():
            repo = RunRepo(session)
            run = repo.get(run_id)
            if run is None:
                raise LookupError(f"Processing run '{run_id}' not found")
            repo.update(run, changes)

    logger.info(
        "Processing stage started: run_id=%s task_id=%s stage=%s",
        run_id,
        task_id,
        stage.value,
    )
    try:
        update_run(
            RunUpdate(
                status=ProcessingStatus.RUNNING,
                stage=stage,
                error_type=None,
                error_message=None,
            )
        )
        yield
        if final_stage:
            update_run(RunUpdate(status=ProcessingStatus.SUCCEEDED))
    except Retry:
        try:
            update_run(RunUpdate(status=ProcessingStatus.RETRYING, stage=stage))
        except Exception:
            logger.exception(
                "Could not persist retry status: run_id=%s task_id=%s",
                run_id,
                task_id,
            )
        logger.warning(
            "Processing stage retry requested: run_id=%s task_id=%s "
            "stage=%s elapsed_seconds=%.2f",
            run_id,
            task_id,
            stage.value,
            perf_counter() - started,
        )
        raise
    except (Ignore, Reject):
        raise
    except Exception as exc:
        logger.exception(
            "Processing stage failed: run_id=%s task_id=%s "
            "stage=%s error_type=%s elapsed_seconds=%.2f",
            run_id,
            task_id,
            stage.value,
            type(exc).__name__,
            perf_counter() - started,
        )
        try:
            update_run(
                RunUpdate(
                    status=ProcessingStatus.FAILED,
                    stage=stage,
                    error_type=type(exc).__name__,
                    error_message=f"Processing failed during {stage.value}",
                )
            )
        except Exception:
            logger.exception(
                "Could not persist failure status: run_id=%s task_id=%s",
                run_id,
                task_id,
            )
        raise
    else:
        logger.info(
            "Processing stage completed: run_id=%s task_id=%s "
            "stage=%s elapsed_seconds=%.2f",
            run_id,
            task_id,
            stage.value,
            perf_counter() - started,
        )
