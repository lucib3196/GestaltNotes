from typing import cast
from uuid import UUID

from backend.accounts.services.role import RoleDB
from firebase_admin import auth
from firebase_admin.auth import UserNotFoundError as FBUserNotFoundError
from firebase_admin.auth import UserRecord
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from backend.accounts.exceptions import (
    UserCreationError,
    UserNotFoundError,
    UserServiceException,
    UserUpdateError,
    UserDeletionError,
    UserRoleLinkError,
    AuthDrift,
    FirebaseAuthError,
)
from backend.accounts.models import User, UserRole
from backend.accounts.schema import UserCreate, UserRead, UserUpdate
from backend.core import logger
from backend.utils.utils import convert_uuid

from backend.shared.types import ID


class AccountService:
    _VALID_ROLE_SET: set[UserRole] = {
        UserRole.EDUCATOR,
        UserRole.STUDENT,
        UserRole.ADMIN,
    }

    def __init__(self, session: Session) -> None:
        self._session = session
        self._role_db = RoleDB(session)

    async def create_account(
        self,
        data: UserCreate,
        role: UserRole | None = UserRole.STUDENT,
        force_password_reset: bool = True,
    ) -> User:
        user_id: ID | None = None
        try:
            user = await self._create_db_user(data)
            if not user.id:
                raise UserCreationError("[DB] Failed to create user")

            user_id = user.id
            self._create_firebase_user(
                user,
                password=data.password,
                force_password_reset=force_password_reset,
            )

            if role:
                await self.assign_role(user, role)

            return user
        except Exception as e:
            if user_id is not None:
                await self._rollback_account_creation(user_id)

            if "EMAIL_EXISTS" in str(e):
                raise UserCreationError("User with this email already exists.") from e
            if isinstance(e, UserCreationError):
                raise
            raise UserServiceException(
                f"[AccountService] Failed to create user {e}"
            ) from e

    async def get_account(self, user_id: ID) -> UserRead:
        user = await self.get_account_orm(user_id)
        return self._to_user_read(user)

    async def get_account_orm(self, user_id: ID) -> User:
        user = await self._get_db_user(user_id)
        if not user:
            raise UserNotFoundError(user_id=str(user_id))
        return user

    async def get_account_by_email(self, email: str) -> User | None:
        try:
            stmt = select(User).where(User.email == email.strip())
            return self._session.exec(stmt).first()
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[AccountService] failed to get user by email {e}"
            logger.error(message)
            raise UserServiceException(message) from e

    async def update_account(self, user_id: ID, data: UserUpdate) -> UserRead:
        user = await self._update_db_user(user_id, data)
        return self._to_user_read(user)

    async def delete_account(self, user_id: ID) -> None:
        errors: list[Exception] = []

        try:
            await self._delete_db_user(user_id)
        except Exception as e:
            errors.append(e)

        try:
            self._delete_firebase_user(user_id)
        except Exception as e:
            errors.append(e)

        if errors:
            raise UserDeletionError(
                f"Failed to delete user {user_id}: {'; '.join(str(e) for e in errors)}"
            )

    async def assign_role(self, user: User | ID, role: UserRole) -> User:
        resolved_user = await self._resolve_user(user)
        role_orm = await self._role_db.get_role(role)
        if not role_orm:
            raise ValueError(f"Role '{role}' not found")

        if role_orm not in resolved_user.roles:
            resolved_user.roles.append(role_orm)

        try:
            self._session.add(resolved_user)
            self._session.commit()
            self._session.refresh(resolved_user)
            return resolved_user
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[AccountService] failed to add role {role} to user. {e}"
            logger.error(message)
            raise UserRoleLinkError(message) from e

    async def list_roles(self, user: User | ID) -> list[UserRole]:
        resolved_user = await self._resolve_user(user)
        roles: list[UserRole] = []
        for role in resolved_user.roles:
            if role.name in self._VALID_ROLE_SET:
                roles.append(cast(UserRole, role.name))
        return roles

    async def _create_db_user(self, data: UserCreate | User) -> User:
        try:
            user = User(
                first_name=data.first_name,
                last_name=data.last_name,
                username=data.username,
                email=data.email,
            )
            self._session.add(user)
            self._session.commit()
            self._session.refresh(user)
            return user
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[AccountService] failed to create user {e}"
            logger.error(message)
            raise UserCreationError(message) from e

    async def _get_db_user(self, user_id: ID) -> User | None:
        try:
            return self._session.exec(
                select(User).where(User.id == convert_uuid(user_id))
            ).first()
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[AccountService] failed to get user {e}"
            logger.error(message)
            raise UserServiceException(message) from e

    async def _update_db_user(self, user_id: ID, data: UserUpdate) -> User:
        user = await self.get_account_orm(user_id)
        try:
            for key, value in data.model_dump(exclude_none=True).items():
                setattr(user, key, value)
            self._session.add(user)
            self._session.commit()
            self._session.refresh(user)
            return user
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[AccountService] failed to update user {e}"
            logger.error(message)
            raise UserUpdateError(message) from e

    async def _delete_db_user(self, user_id: ID) -> bool:
        user = await self.get_account_orm(user_id)
        try:
            self._session.delete(user)
            self._session.commit()
            logger.info(f"[AccountService] deleted db user {user.id}")
            return True
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[AccountService] failed to delete db user {e}"
            logger.error(message)
            raise UserDeletionError(message) from e

    def _create_firebase_user(
        self,
        user: User,
        *,
        password: str,
        force_password_reset: bool = True,
    ) -> UserRecord:
        if not user.id:
            raise UserCreationError("Failed to create Firebase user. User id is None")

        display_name = user.username or f"{user.email.split('@')[0]}_{str(user.id)[:4]}"
        try:
            fb_user = auth.create_user(
                email=user.email,
                display_name=display_name,
                uid=str(user.id),
                password=password,
            )

            if fb_user.uid != str(user.id):
                raise AuthDrift(
                    "Internal database user and firebase user do not contain "
                    f"matching id fb: {fb_user.uid} db: {user.id}"
                )

            if force_password_reset:
                auth.set_custom_user_claims(
                    str(user.id), {"force_password_reset": True}
                )

            return fb_user
        except Exception as e:
            if isinstance(e, AuthDrift):
                raise
            raise FirebaseAuthError(f"Failed to create Firebase user {e}") from e

    def _delete_firebase_user(self, user_id: ID) -> bool:
        try:
            user = auth.get_user(str(user_id))
            auth.delete_user(user.uid)
            logger.info("Deleted firebase user ok")
            return True
        except FBUserNotFoundError:
            logger.info(
                "Attempted to delete firebase user. Firebase user with %s does not exist",
                user_id,
            )
            return True
        except Exception as e:
            raise FirebaseAuthError(f"Failed to delete firebase user {e}") from e

    async def _rollback_account_creation(self, user_id: ID) -> None:
        errors: list[Exception] = []

        try:
            await self._delete_db_user(user_id)
        except UserNotFoundError:
            pass
        except Exception as e:
            errors.append(e)

        try:
            self._delete_firebase_user(user_id)
        except Exception as e:
            errors.append(e)

        if errors:
            raise UserDeletionError(
                f"Failed to rollback user {user_id}: {'; '.join(str(e) for e in errors)}"
            )

    async def _resolve_user(self, user: User | ID) -> User:
        if isinstance(user, User):
            return user
        return await self.get_account_orm(user)

    def _to_user_read(self, user: User) -> UserRead:
        roles = [
            cast(UserRole, role.name)
            for role in user.roles
            if role.name in self._VALID_ROLE_SET
        ]
        return UserRead(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            roles=roles,
        )
