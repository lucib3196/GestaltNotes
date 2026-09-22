"""Centralized SQLModel imports for Alembic metadata discovery."""

from backend.accounts.models import Role, User, UserRole, UserRoleLink
from backend.model.chat import Message, Thread
from backend.model.course import Course, LectureNote, StudentCourseLink
from backend.model.generated_content import GeneratedMCQ
from backend.model.user import UserCourseLink

__all__ = [
    "Course",
    "GeneratedMCQ",
    "LectureNote",
    "Message",
    "Role",
    "StudentCourseLink",
    "Thread",
    "User",
    "UserCourseLink",
    "UserRole",
    "UserRoleLink",
]
