from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from backend.core.logger import logger
from backend.database import SessionDep
from backend.service.chat import ThreadDB


@lru_cache
def get_thread_db(session: SessionDep) -> ThreadDB:
    try:
        logger.debug("Initialized Thread DB")
        return ThreadDB(session)
    except Exception:
        raise ValueError("Failed to initialize Thread DB")


ThreadDBDependency = Annotated[ThreadDB, Depends(get_thread_db)]
