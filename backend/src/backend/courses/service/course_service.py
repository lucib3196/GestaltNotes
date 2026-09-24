from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from backend.accounts.models import User, UserRole
from backend.core import logger
from backend.courses.exceptions import (
    CourseCreationError,
    CourseDeletionError,
    CourseNotFoundError,
    CourseOwnershipError,
    CoursePermissionError,
    CourseRetrievalError,
    CourseUpdateError,
)
from backend.courses.models import Course
from backend.courses.schema import CourseCreate, CourseDelete, CourseUpdate
from backend.shared.types import ID
from backend.utils.utils import convert_uuid
from google.cloud.storage import Bucket
from .storage_service import CourseStorageService


class CourseService:
    def __init__(self, session: Session, storage: CourseStorageService) -> None:
        self._session = session
        self._storage = storage

    async def create_course(self, data: CourseCreate, educator: User) -> Course:
        self._assert_educator(educator)

        if not educator.id:
            raise CourseCreationError("Cannot create course for user without id")

        try:
            course = Course(
                name=data.name,
                discipline=data.discipline,
                description=data.description,
                owner_id=educator.id,
            )
            self._session.add(course)
            self._session.commit()
            self._session.refresh(course)

            course = self._set_course_prefix(course)
            return course
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to create course {e}"
            logger.error(message)
            raise CourseCreationError(message) from e

    async def get_course(self, course_id: ID) -> Course:
        try:
            course = self._session.exec(
                select(Course).where(Course.id == convert_uuid(course_id))
            ).first()
            if not course:
                raise CourseNotFoundError(str(course_id))
            return course
        except CourseNotFoundError:
            raise
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to get course {e}"
            logger.error(message)
            raise CourseRetrievalError(message) from e

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

    async def update_course(
        self,
        course_id: ID,
        data: CourseUpdate,
        educator: User,
    ) -> Course:
        course = await self.assert_course_owner(course_id, educator)

        try:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(course, key, value)

            self._session.add(course)
            self._session.commit()
            self._session.refresh(course)
            return course
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to update course {e}"
            logger.error(message)
            raise CourseUpdateError(message) from e

    async def delete_course(self, course_id: ID, educator: User) -> CourseDelete:
        course = await self.assert_course_owner(course_id, educator)

        try:
            self._session.delete(course)
            self._session.commit()
            return CourseDelete(success=True, info=f"Deleted course {course_id}")
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to delete course {e}"
            logger.error(message)
            raise CourseDeletionError(message) from e

    async def assert_course_owner(self, course_id: ID, educator: User) -> Course:
        self._assert_educator(educator)

        if not educator.id:
            raise CourseOwnershipError("Cannot verify ownership for user without id")

        course = await self.get_course(course_id)
        if course.owner_id != educator.id:
            raise CourseOwnershipError(
                f"User '{educator.id}' does not own course '{course_id}'"
            )

        return course

    def _assert_educator(self, user: User) -> None:
        if not any(role.name == UserRole.EDUCATOR for role in user.roles):
            raise CoursePermissionError("Educator role required")


    def _generate_course_prefix(self, course: Course):
        try:
            course_id = course.id
            if not course_id:
                raise ValueError("Cannot determine course id")
            return self._storage.course_prefix(str(course_id))
        except Exception as e:
            raise ValueError("Failed", e)

    def _set_course_prefix(self, course: Course):
        try:
            course.storage_prefix = self._generate_course_prefix(course)
            self._session.add(course)
            self._session.commit()
            self._session.flush()
            return course
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseService] failed to add course storage {e}"
            logger.error(message)
            raise CourseCreationError(message) from e
