from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select

from backend.adapters import Repository
from backend.courses.exceptions import (
    CourseNotFoundError,
)
from backend.courses.models import Course, CourseUpdate


class CourseRepo(Repository[Course, CourseUpdate]):
    def __init__(self, session: Session) -> None:
        self._session = session

    async def create(self, record: Course) -> Course:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    async def get(self, record_id: UUID) -> Course | None:
        return self._session.exec(select(Course).where(Course.id == record_id)).first()

    async def update(self, record: Course, update: CourseUpdate) -> Course:
        for key, value in update.model_dump(exclude_unset=True).items():
            setattr(record, key, value)

        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    async def update_by_id(self, record_id: UUID, update: CourseUpdate) -> Course:
        course = await self.get(record_id)
        if course is None:
            raise CourseNotFoundError(str(record_id))
        return await self.update(course, update)

    async def delete(self, record_id: UUID) -> None:
        course = await self.get(record_id)
        if course is not None:
            self._session.delete(course)
            self._session.flush()

    async def list(self) -> Sequence[Course]:
        return self._session.exec(select(Course)).all()
