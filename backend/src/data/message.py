from uuid import UUID

from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from src.model.chat import Message
from src.core.logger import logger


class MessageDB:
    def __init__(self, session: Session):
        self.session = session

    async def create_message(
        self,
        thread_id: UUID,
        role: str,
        content: str,
    ) -> Message:
        try:
            msg_orm = Message(
                thread_id=thread_id,
                role=role,
                content=content,
                # created_at handled automatically
            )
            self.session.add(msg_orm)
            self.session.commit()
            self.session.flush()
            return msg_orm
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[MessageDB] failed to create message {e}"
            logger.error(message)
            raise ValueError(message)

    async def get_message(self, id: UUID) -> Message:
        try:
            msg = self.session.exec(select(Message).where(Message.id == id)).first()
            if not msg:
                raise ValueError(f"Could not retrieve message, Message {id} is None")
            return msg
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[MessageDB] failed to get message {e}"
            logger.error(message)
            raise ValueError(message)

    async def list_messages(self, thread_id: UUID) -> list[Message]:
        try:
            stmt = (
                select(Message)
                .where(Message.thread_id == thread_id)
                .order_by(Message.created_at.asc())
            )
            return list(self.session.exec(stmt).all())
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[MessageDB] failed to list messages {e}"
            logger.error(message)
            raise ValueError(message)