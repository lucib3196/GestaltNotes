from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.core.database_config import SessionDep
from src.core.logger import logger
from src.service.chat import ThreadDB

@lru_cache
def get_thread_db(session: SessionDep) -> ThreadDB:
    try:
        logger.debug("Initialized Thread DB")
        return ThreadDB(session)
    except Exception:
        raise ValueError("Failed to initialize Thread DB")


ThreadDBDependency = Annotated[ThreadDB, Depends(get_thread_db)]
