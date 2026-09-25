"""Centralized SQLModel imports for Alembic metadata discovery."""

from backend.accounts.models import Role, User, UserRole, UserRoleLink
from backend.courses.models import (
    Course,
    CourseAccessCode,
    CourseEnrollment,
    LectureNote,
)
from backend.model.chat import Message, Thread
from backend.model.generated_content import GeneratedMCQ
from backend.model.user import UserCourseLink

__all__ = [
    "Course",
    "CourseAccessCode",
    "CourseEnrollment",
    "GeneratedMCQ",
    "LectureNote",
    "Message",
    "Role",
    "Thread",
    "User",
    "UserCourseLink",
    "UserRole",
    "UserRoleLink",
]
