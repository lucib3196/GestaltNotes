from uuid import UUID

from backend.accounts.models import User, UserRole
from backend.courses.exceptions import (
    CourseNotFoundError,
    CourseOwnershipError,
    CoursePermissionError,
)
from backend.courses.models import Course
from backend.courses.repo import CourseRepo


class CourseAccess:
    """Basic checks to assert course permission"""
    def __init__(self, courses: CourseRepo) -> None:
        self._courses = courses

    def require_educator(self, user: User) -> None:
        if not any(role.name == UserRole.EDUCATOR for role in user.roles):
            raise CoursePermissionError("Educator role required")

    async def require_owner(self, course_id: UUID, user: User) -> Course:
        self.require_educator(user)

        if user.id is None:
            raise CourseOwnershipError("Cannot verify ownership for user without id")

        course = await self._courses.get(course_id)
        if course is None:
            raise CourseNotFoundError(str(course_id))

        if course.owner_id != user.id:
            raise CourseOwnershipError(
                f"User '{user.id}' does not own course '{course_id}'"
            )

        return course
