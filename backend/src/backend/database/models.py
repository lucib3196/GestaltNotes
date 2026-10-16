"""Centralized SQLModel imports for Alembic metadata discovery."""

from backend.accounts.models import Role, User, UserRole, UserRoleLink
from backend.chat.model import Message, Thread
from backend.courses.models import (
    Course,
    CourseAccessCode,
    CourseEnrollment,
    CourseNote,
)
from backend.model.generated_content import GeneratedMCQ
from backend.model.user import UserCourseLink
from backend.storage.models import Document, File, FileProcessing, ProcessingStatus

__all__ = [
    "Course",
    "CourseAccessCode",
    "CourseEnrollment",
    "CourseNote",
    "Document",
    "File",
    "FileProcessing",
    "GeneratedMCQ",
    "Message",
    "ProcessingStatus",
    "Role",
    "Thread",
    "User",
    "UserCourseLink",
    "UserRole",
    "UserRoleLink",
]
