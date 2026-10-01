from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from backend.core.logger import logger
from backend.core.settings import get_settings
from backend.data.message import MessageDB
from backend.database import SessionDep





@lru_cache
def get_message_db(session: SessionDep) -> MessageDB:
    try:
        logger.debug("Initialized Message DB")
        return MessageDB(session)
    except Exception:
        raise ValueError("Failed to initialize Message DB")


MessageDBDependency = Annotated[MessageDB, Depends(get_message_db)]
