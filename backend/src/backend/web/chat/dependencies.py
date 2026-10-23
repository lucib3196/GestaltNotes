from typing import Annotated

from fastapi import Depends
from langgraph_sdk import get_client

from backend.chat import ThreadService
from backend.core.settings import get_settings
from backend.database import SessionDep

settings = get_settings()
client = get_client(
    url=settings.LANGGRAPH_STREAM_URL,
    api_key=settings.LANGSMITH_API_KEY,
)


def get_thread_service(session: SessionDep) -> ThreadService:
    return ThreadService(session=session, client=client)


ThreadServiceDependency = Annotated[ThreadService, Depends(get_thread_service)]
