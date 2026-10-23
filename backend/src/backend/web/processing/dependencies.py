from typing import Annotated

from fastapi import Depends

from backend.database import SessionDep
from backend.processing.lecture_processing_service import LectureProcessingService


def get_lecture_processing_service(
    session: SessionDep,
) -> LectureProcessingService:
    return LectureProcessingService(session)


LectureProcessingServiceDep = Annotated[
    LectureProcessingService,
    Depends(get_lecture_processing_service),
]
