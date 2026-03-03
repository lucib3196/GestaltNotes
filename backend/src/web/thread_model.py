from pydantic import BaseModel
from uuid import UUID

class ThreadCreate(BaseModel):
    thread_id: UUID
    user_id: UUID
    course_id: UUID
    title: str | None = None
    agent: str | None = None

class ThreadList(BaseModel):
    user_id: UUID
    course_id: UUID | None = None

class MessageCreate(BaseModel):
    role: str
    content: str