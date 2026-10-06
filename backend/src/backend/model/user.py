from uuid import UUID

from sqlmodel import Field as SqlField
from sqlmodel import SQLModel


class UserCourseLink(SQLModel, table=True):
    user_id: UUID = SqlField(foreign_key="user.id", primary_key=True)
    course_id: UUID = SqlField(foreign_key="course.id", primary_key=True)
