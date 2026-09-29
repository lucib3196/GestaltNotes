from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, select

from backend.accounts import User
from backend.core import logger
from backend.courses.exceptions import (
    CourseNoteAssociationError,
    CourseNoteNotFoundError,
    CourseNoteRetrievalError,
)
from backend.courses.models import CourseNote
from backend.courses.schema import CourseNoteUpdate
from backend.database import Repository


class CourseNoteRepository(Repository[CourseNote, CourseNoteUpdate]):
    def __init__(self, session: Session) -> None:
        self._session = session

    async def create(self, record: CourseNote) -> CourseNote:
        try:
            self._session.add(record)
            self._session.flush()
            self._session.refresh(record)
            return record
        except IntegrityError as e:
            message = f"[CourseNoteRepository] failed to create course note {e}"
            logger.error(message)
            raise CourseNoteAssociationError(message) from e
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to create course note {e}"
            logger.error(message)
            raise CourseNoteAssociationError(message) from e

    async def get(self, record_id: UUID) -> CourseNote | None:
        try:
            return self._session.get(CourseNote, record_id)
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to get course note {e}"
            logger.error(message)
            raise CourseNoteRetrievalError(message) from e

    async def get_by_course_and_file(
        self,
        course_id: UUID,
        file_id: UUID,
    ) -> CourseNote | None:
        try:
            return self._session.exec(
                select(CourseNote)
                .where(CourseNote.course_id == course_id)
                .where(CourseNote.file_id == file_id)
            ).first()
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to get course note {e}"
            logger.error(message)
            raise CourseNoteRetrievalError(message) from e

    async def update(self, record: CourseNote, update: CourseNoteUpdate) -> CourseNote:
        try:
            for key, value in update.model_dump(exclude_unset=True).items():
                setattr(record, key, value)

            self._session.add(record)
            self._session.flush()
            self._session.refresh(record)
            return record
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to update course note {e}"
            logger.error(message)
            raise CourseNoteAssociationError(message) from e

    async def update_by_id(
        self,
        record_id: UUID,
        update: CourseNoteUpdate,
    ) -> CourseNote:
        note = await self.get(record_id)

        if note is None:
            raise CourseNoteNotFoundError("", str(record_id))

        return await self.update(note, update)

    async def delete(self, record_id: UUID) -> None:
        try:
            note = await self.get(record_id)

            if note is None:
                raise CourseNoteNotFoundError("", str(record_id))

            self._session.delete(note)
            self._session.flush()
        except CourseNoteNotFoundError:
            raise
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to delete course note {e}"
            logger.error(message)
            raise CourseNoteAssociationError(message) from e

    async def list_by_course(self, course_id: UUID) -> list[CourseNote]:
        try:
            return list(
                self._session.exec(
                    select(CourseNote).where(CourseNote.course_id == course_id)
                ).all()
            )
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to list course notes {e}"
            logger.error(message)
            raise CourseNoteRetrievalError(message) from e

    async def list_by_owner(self, owner: User) -> list[CourseNote]:
        raise NotImplementedError("Course notes are listed by course, not by owner")
