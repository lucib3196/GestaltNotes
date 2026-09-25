"""Centralized SQLModel imports for Alembic metadata discovery."""

from backend.accounts.models import Role, User, UserRole, UserRoleLink
from backend.courses.models import (
    Course,
    CourseAccessCode,
    CourseEnrollment,
    CourseNote,
)
from backend.model.chat import Message, Thread
from backend.model.generated_content import GeneratedMCQ
from backend.model.user import UserCourseLink
from backend.storage.models import File
__all__ = [
    "Course",
    "CourseAccessCode",
    "CourseEnrollment",
    "GeneratedMCQ",
    "CourseNote",
    "Message",
    "Role",
    "Thread",
    "User",
    "UserCourseLink",
    "UserRole",
    "UserRoleLink",
    "File"
]
