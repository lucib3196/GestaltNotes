from typing import Any
from uuid import UUID

from sqlmodel import Session
from backend.processing.model import (
    ProcessingRun,
    ProcessingStage,
)


class ProcessingRunService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, run_id: UUID) -> ProcessingRun | None:
        return self._session.get(ProcessingRun, run_id)

    def get_or_raise(self, run_id: UUID) -> ProcessingRun:
        run = self.get(run_id)
        if not run:
            raise ValueError("Run Not found")
        return run
    # def start(self, run_id: UUID)->ProcessingRun:
    #     run = ProcessingRun()