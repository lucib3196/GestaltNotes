from firebase_admin import auth
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from src.data.role import RoleDB
from src.model.user import VALID_ROLES, User, UserCreate
from src.core import logger
from .exceptions import UserCreationError, UserRoleLinkError, UserServiceException
from .userdb import UserDB
from uuid import UUID

ID = str | UUID


class UserManager:
    def __init__(self, session: Session) -> None:
        """Initialize user and role data access with a shared database session."""
        self._udb = UserDB(session)
        self._rm = RoleDB(session)
        self._session = session

    async def create_user(
        self,
        data: UserCreate,
        role: VALID_ROLES | None = "student",
        force_password_reset: bool = True,
    ) -> User:
        """Create a user in the database and Firebase, then optionally assign a role.

        Args:
            data: User creation payload containing profile and password fields.
            role: Optional default role to attach after creation.
            force_password_reset: Whether to mark the Firebase user for password reset.

        Returns:
            The created user record from the database.

        Raises:
            UserCreationError: If the database user cannot be created.
            UserServiceException: If any part of the creation workflow fails.
        """
        try:
            user_orm = User(
                first_name=data.first_name, last_name=data.last_name, email=data.email
            )
            user = await self._udb.create_user(data=user_orm)
            if not user:
                raise UserCreationError("[DB] Failed to create user")

            display_name = f"{user_orm.email.split('@')[0]}_{str(user_orm.id)[:4]}"
            # First create the user in the firebase auth
            auth.create_user(
                email=data.email,
                display_name=display_name,
                uid=str(user.id),
                password=data.password,
            )
            if role:
                await self._add_user_role(user_orm, role)

            if force_password_reset:
                auth.set_custom_user_claims(
                    str(user.id), {"force_password_reset": True}
                )

            return user
        except UserServiceException:
            raise
        except Exception as e:
            raise UserServiceException(
                f"[UserManager] Failed to create user {e}"
            ) from e

    async def _add_user_role(self, user: User, role: VALID_ROLES) -> None:
        """Attach a role to an existing user and persist the relationship.

        Args:
            user: Target user ORM object.
            role: Role name to assign.

        Raises:
            UserRoleLinkError: If persisting the role link fails.
        """
        r = await self._rm.get_role(role)
        if not r:
            logger.error(
                "Failed to add role to user. Role may not be present in database"
            )
            return
        user.roles.append(r)
        try:
            self._session.commit()
            self._session.flush()
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[UserManager] failed to add role {role} to user. {e}"
            logger.error(message)
            raise UserRoleLinkError(message) from e

    async def get_user(self, id: ID) -> User | None:
        """Fetch a user by identifier.

        Args:
            id: Internal user identifier.

        Returns:
            The user if found; otherwise `None`.
        """
        return await self._udb.get_user(id)
