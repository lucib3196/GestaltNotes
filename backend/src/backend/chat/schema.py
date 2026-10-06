from uuid import UUID

from pydantic import BaseModel


class ThreadCreate(BaseModel):
    thread_id: UUID | str | None = None
    user_id: UUID | str | None = None
    title: str | None = None
    agent: str | None = None


class ThreadUpdate(BaseModel):
    title: str | None = None


class MessageCreate(BaseModel):
    role: str
    content: str
