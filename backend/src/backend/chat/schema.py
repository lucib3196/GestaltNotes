from uuid import UUID

from pydantic import BaseModel

from backend.chat.model import ThreadTitleSource


class ThreadCreate(BaseModel):
    thread_id: UUID | str | None = None
    user_id: UUID | str | None = None
    title: str | None = None
    agent: str | None = None


class ThreadUpdate(BaseModel):
    title: str | None = None
    title_source: ThreadTitleSource | None = None


class MessageCreate(BaseModel):
    role: str
    content: str
