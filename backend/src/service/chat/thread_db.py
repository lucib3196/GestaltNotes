from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.core.logger import logger
from src.model.chat import Thread, ThreadUpdate
from src.utils.utils import convert_uuid

from .exceptions import (
    ThreadBaseException,
    ThreadCreateError,
    ThreadNotFound,
    ThreadRetrievalError,
    ThreadUpdateError,
)


class ThreadDB:
    """Service-layer database operations for chat threads."""

    def __init__(self, session: Session) -> None:
        """Initialize the thread repository with a SQLModel session."""
        self.session = session

    async def create_thread(
        self,
        user_id: UUID | str,
        thread_id: UUID | str | None = None,
        course_id: UUID | str | None = None,
        title: str | None = None,
        agent: str | None = None,
    ) -> Thread:
        """
        Create and persist a new thread.

        Args:
            user_id: Owner of the thread.
            thread_id: Optional explicit thread identifier.
            course_id: Optional course identifier for scoping.
            title: Optional thread title.
            agent: Optional agent label.

        Returns:
            The created thread ORM object.
        """
        try:
            thread_orm = Thread(
                id=convert_uuid(thread_id) if thread_id else None,
                user_id=convert_uuid(user_id),
                course_id=convert_uuid(course_id) if course_id else None,
                title=title,
                agent=agent,
                # created_at/updated_at handled automatically
            )
            self.session.add(thread_orm)
            self.session.commit()
            self.session.flush()
            return thread_orm
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to create thread {e}"
            logger.error(message)
            raise ThreadCreateError(message)

    async def get_thread(self, id: UUID | str) -> Thread:
        """
        Retrieve a thread by its id.

        Args:
            id: Thread identifier.

        Returns:
            The matching thread.

        Raises:
            ThreadNotFound: If no thread exists for the given id.
        """
        try:
            thread = self.session.exec(
                select(Thread).where(Thread.id == convert_uuid(id))
            ).first()
            if not thread:
                raise ThreadNotFound(f"Could not retrieve thread, Thread {id} is None")
            return thread
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to get thread {e}"
            logger.error(message)
            raise ThreadRetrievalError(message)

    async def update_thread(
        self, thread_id: str | UUID, thread_update: ThreadUpdate
    ) -> Thread:
        try:
            thread = await self.get_thread(thread_id)
            if thread_update.title:
                thread.title = thread_update.title
            self.session.add(thread)
            self.session.commit()
            self.session.flush()
            return thread
        except ThreadBaseException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to update thread {e}"
            logger.error(message)
            raise ThreadUpdateError(message) from e

    async def get_thread_for_user(
        self, user_id: UUID | str, thread_id: UUID | str
    ) -> Thread:
        """
        Retrieve a single thread owned by a specific user.

        Args:
            user_id: User identifier.
            thread_id: Thread identifier.

        Returns:
            The matching thread for the user.

        Raises:
            ThreadNotFound: If the thread does not exist for the given user.
            ThreadRetrievalError: If a database error occurs while fetching.
        """
        try:
            stmt = select(Thread).where(
                Thread.id == convert_uuid(thread_id),
                Thread.user_id == convert_uuid(user_id),
            )
            thread = self.session.exec(stmt).first()
            if not thread:
                raise ThreadNotFound(
                    f"Could not retrieve thread {thread_id} for user {user_id}"
                )
            return thread
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to get user thread {e}"
            logger.error(message)
            raise ThreadRetrievalError(message) from e

    async def list_threads_for_user(
        self,
        user_id: UUID | str,
        course_id: UUID | None = None,
    ) -> list[Thread]:
        """
        List all threads for a user, optionally filtered by course.

        Results are sorted by most recently updated first.
        """
        try:
            stmt = select(Thread).where(Thread.user_id == convert_uuid(user_id))
            if course_id is not None:
                stmt = stmt.where(Thread.course_id == course_id)
            stmt = stmt.order_by(Thread.updated_at.desc())  # type: ignore
            return list(self.session.exec(stmt).all())
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to list threads {e}"
            logger.error(message)
            raise ThreadRetrievalError(message)

    async def touch_updated_at(self, id: UUID | str) -> Thread:
        """
        Update a thread's `updated_at` timestamp to the current UTC time.

        This is used to keep recently accessed threads ordered at the top.

        Args:
            id: Thread identifier.

        Returns:
            The updated thread.
        """
        try:
            thread = await self.get_thread(convert_uuid(id))
            thread.updated_at = datetime.utcnow()
            self.session.add(thread)
            self.session.commit()
            self.session.flush()
            return thread
        except ThreadBaseException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to update thread timestamp {e}"
            logger.error(message)
            raise ThreadUpdateError(message)
