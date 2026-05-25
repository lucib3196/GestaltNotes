from firebase_admin import auth
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from src.data.role import RoleDB
from src.model.user import VALID_ROLES, User, UserCreate

from . import ID, logger
from .exceptions import UserCreationError, UserRoleLinkError, UserServiceException
from .userdb import UserDB


class UserManager:
    def __init__(self, session: Session) -> None:
        self._udb = UserDB(session)
        self._rm = RoleDB(session)
        self._session = session

    async def create_user(
        self,
        data: UserCreate,
        role: VALID_ROLES | None = "student",
        force_password_reset: bool = True,
    ) -> User:
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
        """Fetches the users data

        Args:
            id (ID): _description_

        Returns:
            User|None: _description_
        """
        return await self._udb.get_user(id)
