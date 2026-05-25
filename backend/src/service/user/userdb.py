from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.core.logger import logger
from src.model.user import User, UserCreate, UserUpdate
from src.utils.utils import convert_uuid

from . import ID
from .exceptions import (
    UserCreationError,
    UserNotFoundError,
    UserServiceException,
    UserUpdateError,
)


class UserDB:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create_user(self, data: UserCreate | User) -> User | None:
        try:
            user_orm = User(
                first_name=data.first_name, last_name=data.last_name, email=data.email
            )
            self.session.add(user_orm)
            self.session.commit()
            self.session.flush()
            return user_orm
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[UserDB] failed to create user {e}"
            logger.error(message)
            raise UserCreationError(message) from e

    async def get_user(self, id: ID) -> User | None:
        try:
            return self.session.exec(
                select(User).where(User.id == convert_uuid(id))
            ).first()
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[UserDB] failed to get user {e}"
            logger.error(message)
            raise UserServiceException(message) from e

    async def get_user_by_email(self, email: str) -> User | None:
        try:
            stmt = select(User).where(User.email == email.strip())
            return self.session.exec(stmt).first()
        except Exception as e:
            self.session.rollback()
            error_message = f"[DB] Failed to get user: {e}"
            logger.error(error_message)
            raise UserNotFoundError(error_message) from e

    async def delete_user(self, id: ID) -> bool:

        user = await self.get_user(id)
        if not user:
            raise UserNotFoundError(user_id=str(id), message="Failed to delete user")

        try:
            self.session.delete(user)
            self.session.commit()
            logger.info(f"[DB] Deleted user {user.id} successfully")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            error_message = f"[DB] Failed to delete user: {e}"
            logger.error(error_message)
            raise ValueError(error_message) from e

    async def update_user(self, id: ID, data: UserUpdate):
        user = await self.get_user(id)
        if not user:
            raise UserNotFoundError(user_id=str(id), message="Failed to delete user")
        try:
            for key, value in data.model_dump(exclude_none=True).items():
                setattr(user, key, value)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"[DB] Failed to edit user: {e}")
            raise UserUpdateError(f"[DB] Failed to edit user: {e}") from e
