from typing import Union, cast
from uuid import UUID

from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError as FBUserNotFoundError, UserRecord
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from src.core import logger
from src.data.role import RoleDB
from src.model.user import VALID_ROLES, User, UserCreate, UserRead, UserUpdate

from .exceptions import (
    AuthDrift,
    FirebaseAuthError,
    UserCreationError,
    UserDeletionError,
    UserNotFoundError,
    UserRoleLinkError,
    UserServiceException,
)
from .userdb import UserDB

ID = str | UUID


class UserManager:
    _VALIDE_ROLE_SET: set[VALID_ROLES] = {"educator", "student", "admin"}

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
        user_id: ID | None = None
        try:
            user_orm = User(
                first_name=data.first_name, last_name=data.last_name, email=data.email
            )
            user = await self._udb.create_user(data=user_orm)
            if not user or not user.id:
                raise UserCreationError("[DB] Failed to create user")

            user_id = user.id
            display_name = f"{data.email.split('@')[0]}_{str(user_id)[:4]}"

            logger.debug(f"Created user with {user_id}")
            fb_user: UserRecord = auth.create_user(
                email=data.email,
                display_name=display_name,
                uid=str(user_id),
                password=data.password,
            )

            if fb_user.uid != str(user_id):
                raise AuthDrift(
                    f"Internal database user and firebase user do not contain matching id fb: {fb_user.uid} db: {user_id}"
                )
            if role:
                await self.set_user_roles(user, role)

            if force_password_reset:
                auth.set_custom_user_claims(
                    str(user_id), {"force_password_reset": True}
                )

            return user
        except Exception as e:
            if user_id is not None:
                await self.rollback_user(user_id)
                await self.ensure_user_rolled_back(user_id)

            if "EMAIL_EXISTS" in str(e):
                raise UserCreationError("User with this email already exists.") from e
            raise UserServiceException(
                f"[UserManager] Failed to create user {e}"
            ) from e

    async def get_user(self, id: ID) -> UserRead:
        """Fetch a user by identifier.

        Args:
            id: Internal user identifier.

        Returns:
            The user if found; otherwise `None`.
        """
        user = await self._udb.get_user(id)

        if not user:
            raise UserNotFoundError(user_id=str(id))
        roles = user.roles

        cleaned_roles: list[VALID_ROLES] = []
        for r in roles:
            if r.name in self._VALIDE_ROLE_SET:
                cleaned_roles.append(cast(VALID_ROLES, r.name))
        return UserRead(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            roles=cleaned_roles,
        )

    async def update_user(self, id: ID, update: UserUpdate) -> UserRead:
        await self._udb.update_user(id, update)
        logger.debug("Update user ok")
        return await self.get_user(id)

    async def delete_user(self, id: ID) -> None:
        try:
            await self._udb.delete_user(id)
        except Exception as e:
            raise UserDeletionError(f"Failed to delete user {e}") from e

    async def rollback_user(self, id: ID) -> None:
        errors: list[Exception] = []

        try:
            await self.rollback_db(id)
        except Exception as e:
            errors.append(e)

        try:
            await self.rollback_fb(id)
        except Exception as e:
            errors.append(e)

        if errors:
            raise UserDeletionError(
                f"Failed to rollback user {id}: {'; '.join(str(e) for e in errors)}"
            )

    async def ensure_user_rolled_back(self, id: ID) -> None:
        db_user = await self._udb.get_user(id)
        if db_user:
            raise UserDeletionError(f"Rollback failed: database user {id} still exists")

        try:
            auth.get_user(str(id))
        except FBUserNotFoundError:
            return
        except Exception as e:
            raise FirebaseAuthError(
                f"Failed to verify firebase rollback for user {id}: {e}"
            ) from e

        raise UserDeletionError(f"Rollback failed: firebase user {id} still exists")

    async def rollback_db(self, id: ID) -> bool:
        try:
            await self._udb.delete_user(id)
            return True
        except UserNotFoundError:
            return True
        except Exception as e:
            raise UserDeletionError(f"Failed to delete user {e}")

    async def rollback_fb(self, id: ID) -> bool:
        try:
            user: UserRecord = auth.get_user(str(id))
            auth.delete_user(user.uid)
            logger.info("Rolledback firebase user ok")
            return True
        except FBUserNotFoundError as e:
            logger.info(
                f"Attempted to delete firebase user. Firebase user with {id} does not exist"
            )
            return True
        except Exception as e:
            raise FirebaseAuthError(f"Failed to delete firebase user {e}") from e

    async def set_user_roles(
        self, user: Union["User", ID], role: VALID_ROLES
    ) -> User | None:
        """Attach a role to an existing user and persist the relationship.

        Args:
            user: Target user ORM object.
            role: Role name to assign.

        Raises:
            UserRoleLinkError: If persisting the role link fails.
        """
        user = await self._resolve_user(user)
        r = await self._rm.get_role(role)
        if not r:
            raise ValueError(f"Role '{role}' not found")
        # Avoid duplicates
        if r not in user.roles:
            user.roles.append(r)
        try:
            self._session.commit()
            self._session.flush()
            return user
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[UserManager] failed to add role {role} to user. {e}"
            logger.error(message)
            raise UserRoleLinkError(message) from e

    async def get_user_roles(self, user: Union["User", ID]) -> list[VALID_ROLES]:
        user = await self._resolve_user(user)
        roles = user.roles
        cleaned_roles: list[VALID_ROLES] = []
        for r in roles:
            if r.name in self._VALIDE_ROLE_SET:
                cleaned_roles.append(cast(VALID_ROLES, r.name))
        return cleaned_roles

    async def _resolve_user(self, user: Union["User", ID]) -> User:
        if isinstance(user, User):
            return user
        u = await self._udb.get_user(user)
        if not u:
            raise UserNotFoundError(user_id=str(id))
        return u
