from datetime import datetime
from typing import Any
from uuid import UUID

from httpx import HTTPStatusError
from langgraph_sdk.client import LangGraphClient
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from backend.chat.exceptions import (
    ThreadClientDeleteError,
    ThreadCreateError,
    ThreadDeleteCommitError,
    ThreadDeleteError,
    ThreadMessageRetrievalError,
    ThreadNotFound,
    ThreadRetrievalError,
    ThreadUpdateError,
)
from backend.chat.model import Message, Thread
from backend.chat.schema import ThreadUpdate
from backend.core.logger import logger
from backend.utils.utils import convert_uuid


class ThreadService:
    """Service-layer database operations for chat threads."""

    def __init__(self, session: Session, client: LangGraphClient) -> None:
        """Initialize the thread repository with a SQLModel session."""
        self.session = session
        self.client = client

    async def create_thread(
        self,
        user_id: UUID | str,
        thread_id: UUID | str | None = None,
        title: str | None = None,
        agent: str | None = None,
    ) -> Thread:
        """
        Create and persist a new thread.

        Args:
            user_id: Owner of the thread.
            thread_id: Optional explicit thread identifier.
            title: Optional thread title.
            agent: Optional agent label.

        Returns:
            The created thread ORM object.
        """
        try:
            thread_orm = Thread(
                id=convert_uuid(thread_id) if thread_id else None,
                user_id=convert_uuid(user_id),
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
            message = f"[ThreadService] failed to create thread {e}"
            logger.error(message)
            raise ThreadCreateError(message) from e

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
            message = f"[ThreadService] failed to get thread {e}"
            logger.error(message)
            raise ThreadRetrievalError(message) from e

    async def delete_thread(self, user_id: UUID | str, thread_id: UUID | str) -> None:
        """Delete SQL rows first, then remote state, then commit SQL.

        Remote failures roll back SQL. A final commit failure cannot restore
        remote state and raises ThreadDeleteCommitError for reconciliation.
        """
        thread = await self.assert_thread_owner(user_id, thread_id)
        remote_id = str(thread.id)
        try:
            self.session.exec(delete(Thread).where(Thread.id == thread.id))  # type: ignore
            self.session.flush()
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.exception("SQL deletion failed for thread %s", thread_id)
            raise ThreadDeleteError("Failed to delete thread") from exc

        try:
            await self.client.threads.delete(remote_id)
        except HTTPStatusError as exc:
            if exc.response.status_code != 404:
                self.session.rollback()
                logger.exception("Remote deletion failed for thread %s", thread_id)
                raise ThreadClientDeleteError("Failed to delete remote thread") from exc
        except Exception as exc:
            self.session.rollback()
            logger.exception("Remote deletion failed for thread %s", thread_id)
            raise ThreadClientDeleteError("Failed to delete remote thread") from exc

        try:
            self.session.commit()
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.exception(
                "SQL commit failed after remote deletion for thread %s", thread_id
            )
            raise ThreadDeleteCommitError(
                "Remote thread deleted, but local deletion failed"
            ) from exc

    async def assert_thread_owner(
        self, user_id: UUID | str, thread_id: UUID | str
    ) -> Thread:
        """Return the owned thread or raise ThreadNotFound."""
        return await self.get_thread_for_user(user_id, thread_id)

    async def update_thread(
        self,
        user_id: UUID | str,
        thread_id: UUID | str,
        thread_update: ThreadUpdate,
    ) -> Thread:
        thread = await self.assert_thread_owner(user_id, thread_id)
        try:
            changes = thread_update.model_dump(exclude_unset=True)
            if not changes:
                return thread
            for field, value in changes.items():
                setattr(thread, field, value)
            thread.updated_at = datetime.utcnow()
            self.session.add(thread)
            self.session.commit()
            return thread
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.exception("Failed to update thread %s", thread_id)
            raise ThreadUpdateError("Failed to update thread") from exc

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
            message = f"[ThreadService] failed to get user thread {e}"
            logger.error(message)
            raise ThreadRetrievalError(message) from e

    async def list_threads_for_user(
        self,
        user_id: UUID | str,
    ) -> list[Thread]:
        """
        List all threads for a user.

        Results are sorted by most recently updated first.
        """
        try:
            stmt = select(Thread).where(Thread.user_id == convert_uuid(user_id))
            stmt = stmt.order_by(Thread.updated_at.desc())  # type: ignore
            return list(self.session.exec(stmt).all())
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadService] failed to list threads {e}"
            logger.error(message)
            raise ThreadRetrievalError(message) from e

    async def touch_updated_at(
        self, user_id: UUID | str, thread_id: UUID | str
    ) -> Thread:
        thread = await self.assert_thread_owner(user_id, thread_id)
        try:
            thread.updated_at = datetime.utcnow()
            self.session.add(thread)
            self.session.commit()
            return thread
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.exception("Failed to update timestamp for %s", thread_id)
            raise ThreadUpdateError("Failed to update thread timestamp") from exc

    async def get_messages(
        self, user_id: UUID | str, thread_id: UUID | str
    ) -> list[dict[str, Any]]:
        thread = await self.assert_thread_owner(user_id, thread_id)
        try:
            data = await self.client.threads.get(str(thread.id))
            values = data.get("values")
            if values is None:
                return []
            if not isinstance(values, dict):
                raise ValueError("Unexpected thread state")
            messages = values.get("messages", [])
            if not isinstance(messages, list) or any(
                not isinstance(message, dict) for message in messages
            ):
                raise ValueError("Unexpected thread messages")
            return messages
        except Exception as exc:
            logger.exception("Failed to retrieve LangGraph messages for %s", thread_id)
            raise ThreadMessageRetrievalError(
                "Failed to retrieve thread messages"
            ) from exc
