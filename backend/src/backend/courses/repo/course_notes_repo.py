from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, col, select

from backend.accounts import User
from backend.adapters import Repository
from backend.core import logger
from backend.courses.exceptions import (
    CourseNoteAssociationError,
    CourseNoteNotFoundError,
    CourseNoteRetrievalError,
)
from backend.courses.models import Course, CourseNote, CourseNoteRead, CourseNoteUpdate


class CourseNoteRepository(Repository[CourseNote, CourseNoteUpdate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, CourseNote)

    async def create(self, record: CourseNote) -> CourseNote:
        try:
            return await super().create(record)
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
            return await super().get(record_id)
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to get course note {e}"
            logger.error(message)
            raise CourseNoteRetrievalError(message) from e

    async def get_required(self, record_id: UUID) -> CourseNote:
        note = await self.get(record_id)
        if note is None:
            raise CourseNoteNotFoundError("", str(record_id))
        return note

    async def get_note_read(self, record_id: UUID) -> CourseNoteRead:
        return self.to_note_read(await self.get_required(record_id))

    async def get_by_course_and_note(
        self,
        course_id: UUID,
        note_id: UUID,
    ) -> CourseNote | None:
        try:
            return self._session.exec(
                select(CourseNote)
                .where(CourseNote.id == note_id)
                .where(CourseNote.course_id == course_id)
            ).first()
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
        try:
            stmt = (
                select(CourseNote)
                .join(Course, col(Course.id) == CourseNote.course_id)
                .where(col(Course.owner_id) == owner.id)
            )
            return list(self._session.exec(stmt).all())
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to list owned notes {e}"
            logger.error(message)
            raise CourseNoteRetrievalError(message) from e

    async def update(self, record: CourseNote, update: CourseNoteUpdate) -> CourseNote:
        try:
            return await super().update(record, update)
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

            await super().delete(record_id)
        except CourseNoteNotFoundError:
            raise
        except SQLAlchemyError as e:
            message = f"[CourseNoteRepository] failed to delete course note {e}"
            logger.error(message)
            raise CourseNoteAssociationError(message) from e

    def to_note_read(self, note: CourseNote) -> CourseNoteRead:
        if note.id is None:
            raise CourseNoteAssociationError("Cannot serialize note without id")

        return CourseNoteRead(
            id=note.id,
            course_id=note.course_id,
            file_id=note.file_id,
            title=note.title,
            resource_type=note.resource_type,
            content_type=note.file.content_type if note.file else None,
        )
