"""Centralized SQLModel imports for Alembic metadata discovery."""

from backend.accounts.models import Role, User, UserRole, UserRoleLink
from backend.model.chat import Message, Thread

from backend.model.generated_content import GeneratedMCQ
from backend.model.user import UserCourseLink
from backend.courses.models import (
    LectureNote,
    CourseEnrollment,
    CourseAccessCode,
    Course,
)

__all__ = [
    "GeneratedMCQ",
    "LectureNote",
    "CourseEnrollment",
    "CourseAccessCode",
    "Course",
    "Message",
    "Role",
    "Thread",
    "User",
    "UserCourseLink",
    "UserRole",
    "UserRoleLink",
]
