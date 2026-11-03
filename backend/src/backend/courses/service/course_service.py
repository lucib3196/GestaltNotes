from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from backend.accounts.models import User
from backend.core import logger
from backend.courses.exceptions import (
    CourseCreationError,
    CourseDeletionError,
    CourseNotFoundError,
    CourseRetrievalError,
    CourseUpdateError,
)
from backend.courses.models import Course, CourseCreate, CourseUpdate
from backend.courses.repo import CourseRepo
from backend.courses.schema import CourseDelete
from backend.courses.access import CourseAccess


class CourseService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._course = CourseRepo(session)
        self._access = CourseAccess(self._course)

    async def create(self, data: CourseCreate, educator: User) -> Course:
        self._assert_educator(educator)
        try:
            assert educator.id
            course = Course(
                name=data.name,
                discipline=data.discipline,
                description=data.description,
                owner_id=educator.id,
            )
            await self._course.create(course)
            self._session.commit()
            return course
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to create course {e}"
            logger.error(message)
            raise CourseCreationError(message) from e

    async def get(self, course_id: UUID) -> Course:
        course = await self._course.get(course_id)
        if not course:
            raise CourseNotFoundError(str(course_id))
        return course

    async def update(
        self, course_id: UUID, update: CourseUpdate, educator: User
    ) -> Course:
        course = await self.assert_course_owner(course_id, educator)
        try:
            course = await self._course.update(course, update)
            self._session.commit()
            return course
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to update course {e}"
            logger.error(message)
            raise CourseUpdateError(message) from e

    async def list_owned_courses(self, educator: User) -> list[Course]:
        self._assert_educator(educator)

        if not educator.id:
            raise CourseRetrievalError("Cannot list courses for user without id")

        try:
            return list(
                self._session.exec(
                    select(Course).where(Course.owner_id == educator.id)
                ).all()
            )
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to list owned courses {e}"
            logger.error(message)
            raise CourseRetrievalError(message) from e

    async def delete(self, course_id: UUID, educator: User) -> CourseDelete:
        await self.assert_course_owner(course_id, educator)
        try:
            await self._course.delete(course_id)
            self._session.commit()
            return CourseDelete(success=True, info=f"Deleted course {course_id}")
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to delete course {e}"
            logger.error(message)
            raise CourseDeletionError(message) from e

    async def assert_course_owner(self, course_id: UUID, educator: User) -> Course:
        return await self._access.require_owner(course_id, educator)

    def _assert_educator(self, user: User) -> None:
        return self._access.require_educator(user)
