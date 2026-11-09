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
        super().__init__(session, Course)

    async def update_by_id(self, record_id: UUID, update: CourseUpdate) -> Course:
        course = await self.get(record_id)
        if course is None:
            raise CourseNotFoundError(str(record_id))
        return await self.update(course, update)

    async def list(self) -> Sequence[Course]:
        return self._session.exec(select(Course)).all()
