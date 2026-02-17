from sqlmodel import Session, select
from src.model.course import Course, CourseData

from sqlalchemy.exc import SQLAlchemyError
from . import logger, ID, convert_uuid


class CourseDB:
    def __init__(self, session: Session):
        self.session = session

    async def create_course(self, data: CourseData) -> Course:
        try:
            course_orm = Course(
                name=data.name,
                discipline=data.name,
                blob=data.blob,
                description=data.description,
            )
            self.session.add(course_orm)
            self.session.commit()
            self.session.flush()
            return course_orm
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[UserDB] failed to create user {e}"
            logger.error(message)
            raise ValueError(message)

    async def get_course(self, id: ID) -> Course:
        try:
            course = self.session.exec(
                select(Course).where(Course.id == convert_uuid(id))
            ).first()
            if not course:
                raise ValueError(f"Could not retreive course, Course {id} is None")
            return course
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[UserDB] failed to get user {e}"
            logger.error(message)
            raise ValueError(message)

    async def set_course_blob(self, id: ID, target: str) -> None:
        try:
            course = await self.get_course(id)
            course.blob = target

            self.session.add(course)
            self.session.commit()
            self.session.flush()
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[UserDB] failed to get set course id {e}"
            logger.error(message)
            raise ValueError(message)

    async def get_course_blob(self, id: ID, target: str) -> str | None:
        try:
            course = await self.get_course(id)
            return course.blob
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[UserDB] failed to get set course id {e}"
            logger.error(message)
            raise ValueError(message)
