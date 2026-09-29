from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, select

from backend.core import logger
from backend.courses.exceptions import (
    CourseNoteAssociationError,
    CourseNoteNotFoundError,
    CourseNoteRetrievalError,
)
from backend.courses.models import Course, CourseContentType, CourseNote
from backend.storage.models import File


class CourseNoteService:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def add_file_to_course(
        self,
        course: Course,
        file: File,
        *,
        resource_type: CourseContentType = CourseContentType.OTHER,
        title: str | None = None,
    ) -> CourseNote:
        """Add a file to a course and commit immediately."""
        try:
            course_note = await self.stage_file_for_course(
                course=course,
                file=file,
                resource_type=resource_type,
                title=title,
            )
            self._session.commit()
            return course_note
        except Exception:
            self._session.rollback()
            raise

    async def stage_file_for_course(
        self,
        course: Course,
        file: File,
        *,
        resource_type: CourseContentType = CourseContentType.OTHER,
        title: str | None = None,
    ) -> CourseNote:
        """Stage a course note in the current transaction."""
        if not course.id:
            raise CourseNoteAssociationError("Cannot add file to course without id")
        if not file.id:
            raise CourseNoteAssociationError("Cannot add file without id")

        try:
            course_note = CourseNote(
                course_id=course.id,
                file_id=file.id,
                resource_type=resource_type,
                title=title or file.original_name,
            )
            self._session.add(course_note)
            self._session.flush()
            self._session.refresh(course_note)
            return course_note
        except IntegrityError as e:
            message = f"[CourseNoteService] failed to associate file with course {e}"
            logger.error(message)
            raise CourseNoteAssociationError(message) from e
        except SQLAlchemyError as e:
            message = f"[CourseNoteService] failed to add course note {e}"
            logger.error(message)
            raise CourseNoteAssociationError(message) from e

    async def remove_file_from_course(
        self,
        course_id: UUID,
        file_id: UUID,
    ) -> None:
        """Remove a file from a course and commit immediately."""
        try:
            await self.stage_remove_file_from_course(course_id, file_id)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    async def stage_remove_file_from_course(
        self,
        course_id: UUID,
        file_id: UUID,
    ) -> None:
        """Stage removal of a course note in the current transaction."""
        try:
            course_note = self._session.exec(
                select(CourseNote)
                .where(CourseNote.course_id == course_id)
                .where(CourseNote.file_id == file_id)
            ).first()

            if not course_note:
                raise CourseNoteNotFoundError(str(course_id), str(file_id))

            self._session.delete(course_note)
            self._session.flush()

        except CourseNoteNotFoundError:
            raise
        except SQLAlchemyError as e:
            message = f"[CourseNoteService] failed to remove course note {e}"
            logger.error(message)
            raise CourseNoteAssociationError(message) from e

    async def list_course_notes(self, course_id: UUID) -> list[CourseNote]:
        try:
            return list(
                self._session.exec(
                    select(CourseNote).where(CourseNote.course_id == course_id)
                ).all()
            )
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseNoteService] failed to list course notes {e}"
            logger.error(message)
            raise CourseNoteRetrievalError(message) from e
