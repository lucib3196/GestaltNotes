from datetime import datetime
from uuid import UUID

from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from src.model.chat import Thread
from src.core.logger import logger


class ThreadDB:
    def __init__(self, session: Session):
        self.session = session

    async def create_thread(
        self,
        user_id: UUID,
        course_id: UUID,
        title: str | None = None,
        agent: str | None = None,
    ) -> Thread:
        try:
            thread_orm = Thread(
                user_id=user_id,
                course_id=course_id,
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
            raise ValueError(message)

    async def get_thread(self, id: UUID) -> Thread:
        try:
            thread = self.session.exec(select(Thread).where(Thread.id == id)).first()
            if not thread:
                raise ValueError(f"Could not retrieve thread, Thread {id} is None")
            return thread
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to get thread {e}"
            logger.error(message)
            raise ValueError(message)

    async def list_threads_for_user(
        self,
        user_id: UUID,
        course_id: UUID | None = None,
    ) -> list[Thread]:
        try:
            stmt = select(Thread).where(Thread.user_id == user_id)
            if course_id is not None:
                stmt = stmt.where(Thread.course_id == course_id)
            stmt = stmt.order_by(Thread.updated_at.desc())
            return list(self.session.exec(stmt).all())
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to list threads {e}"
            logger.error(message)
            raise ValueError(message)

    async def touch_updated_at(self, id: UUID) -> Thread:
        """Bump updated_at so this thread sorts as 'most recent'."""
        # Used for when a thread is accessed, so it shows up as most recent in the UI. We want threads to sort by last used time, not creation time.
        try:
            thread = await self.get_thread(id)
            thread.updated_at = datetime.utcnow()
            self.session.add(thread)
            self.session.commit()
            self.session.flush()
            return thread
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ThreadDB] failed to update thread timestamp {e}"
            logger.error(message)
            raise ValueError(message)