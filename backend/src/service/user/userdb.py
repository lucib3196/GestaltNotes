from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.core import logger
from src.model.user import User, UserCreate, UserUpdate
from src.utils.utils import convert_uuid

from .exceptions import (
    UserCreationError,
    UserNotFoundError,
    UserServiceException,
    UserUpdateError,
)

ID = str | UUID


class UserDB:
    def __init__(self, session: Session) -> None:
        """Initialize user data access with a database session."""
        self.session = session

    async def create_user(self, data: UserCreate | User) -> User | None:
        """Create and persist a user record.

        Args:
            data: User input model containing first name, last name, and email.

        Returns:
            The created user ORM instance, or `None` if creation did not produce a record.

        Raises:
            UserCreationError: If the database insert fails.
        """
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
        """Fetch a user by internal identifier.

        Args:
            id: Internal user identifier.

        Returns:
            The matching user, or `None` when not found.

        Raises:
            UserServiceException: If the database query fails.
        """
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
        """Fetch a user by email address.

        Args:
            email: User email address.

        Returns:
            The matching user, or `None` when not found.

        Raises:
            UserNotFoundError: If the lookup operation fails unexpectedly.
        """
        try:
            stmt = select(User).where(User.email == email.strip())
            return self.session.exec(stmt).first()
        except Exception as e:
            self.session.rollback()
            error_message = f"[DB] Failed to get user: {e}"
            logger.error(error_message)
            raise UserNotFoundError(error_message) from e

    async def delete_user(self, id: ID) -> bool:
        """Delete a user by identifier.

        Args:
            id: Internal user identifier.

        Returns:
            `True` when deletion succeeds.

        Raises:
            UserNotFoundError: If the target user does not exist.
            ValueError: If the delete transaction fails.
        """

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
        """Update mutable fields for a user.

        Args:
            id: Internal user identifier.
            data: Partial user update payload.

        Returns:
            The updated user ORM instance.

        Raises:
            UserNotFoundError: If the target user does not exist.
            UserUpdateError: If persisting updates fails.
        """
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
