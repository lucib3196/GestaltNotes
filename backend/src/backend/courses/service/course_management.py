from uuid import UUID

from authorization import AccessDeniedError, RoleAccessDeniedError
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
from backend.courses.models import Course, CourseCreate, CourseDelete, CourseUpdate
from backend.courses.repo.course_repo import CourseRepo
from backend.courses.service.course_access_gate import CourseOwnershipAccessGate


class CourseManagementService:
    """Manage courses with educator and ownership checks."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._courses = CourseRepo(session)
        self._access = CourseOwnershipAccessGate()

    async def create(self, data: CourseCreate, educator: User) -> Course:
        self.assert_educator(educator)
        try:
            course = Course(
                name=data.name,
                discipline=data.discipline,
                description=data.description,
                owner_id=educator.id,
            )
            await self._courses.create(course)
            self._session.commit()
            return course
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseManagementService] failed to create course {e}"
            logger.error(message)
            raise CourseCreationError(message) from e

    async def get(self, course_id: UUID) -> Course:
        """Load a course for trusted callers; this method does not authorize reads."""
        course = await self._courses.get(course_id)
        if not course:
            raise CourseNotFoundError(str(course_id))
        return course

    async def update(
        self, course_id: UUID, update: CourseUpdate, educator: User
    ) -> Course:
        course = await self.assert_course_owner(course_id, educator)
        try:
            course = await self._courses.update(course, update)
            self._session.commit()
            return course
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseManagementService] failed to update course {e}"
            logger.error(message)
            raise CourseUpdateError(message) from e

    async def list_owned_courses(self, educator: User) -> list[Course]:
        self.assert_educator(educator)

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
            message = f"[CourseManagementService] failed to list owned courses {e}"
            logger.error(message)
            raise CourseRetrievalError(message) from e

    async def delete(self, course_id: UUID, educator: User) -> CourseDelete:
        await self.assert_course_owner(course_id, educator)
        try:
            # TODO: Clean up course notes, stored files, and vectors on deletion.
            await self._courses.delete(course_id)
            self._session.commit()
            return CourseDelete(success=True, info=f"Deleted course {course_id}")
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseManagementService] failed to delete course {e}"
            logger.error(message)
            raise CourseDeletionError(message) from e

    async def require_owner(self, course_id: UUID, user: User) -> Course:
        """Load a course and require an educator who owns it."""
        self.assert_educator(user)
        course = await self.get(course_id)
        self.assert_owner(user, course)
        return course

    async def assert_course_owner(self, course_id: UUID, educator: User) -> Course:
        """Retain the existing ID-based ownership helper."""
        return await self.require_owner(course_id, educator)

    def assert_educator(self, user: User) -> None:
        """Require the educator role using the course gate."""
        try:
            self._access.require_roles(user, allowed_roles=[UserRole.EDUCATOR])
        except RoleAccessDeniedError as exc:
            raise CoursePermissionError("Educator role required") from exc

    def require_educator(self, user: User) -> None:
        """Retain the role-check interface used by enrollment operations."""
        self.assert_educator(user)

    def assert_owner(self, user: User, course: Course) -> None:
        """Require ownership of the supplied course."""
        try:
            self._access.require_ownership(user, course)
        except AccessDeniedError as exc:
            raise CourseOwnershipError(
                f"User '{user.id}' does not own course '{course.id}'"
            ) from exc
