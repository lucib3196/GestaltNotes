from src.data.user import UserDB
from src.model.user import User, UserCreate
from firebase_admin import auth
from sqlmodel import Session
from uuid import UUID
from src.model.user import User, UserCreate, VALID_ROLES
from src.data.role import RoleDB
from . import ID, logger


class UserManager:
    def __init__(self, session: Session):
        self.udb = UserDB(session)
        self.rm = RoleDB(session)

    async def create_user(
        self, data: UserCreate, role: VALID_ROLES | None = "student"
    ) -> User:

        try:
            user_orm = User(
                first_name=data.first_name, last_name=data.last_name, email=data.email
            )
            display_name = (
                f"{user_orm.first_name}_{user_orm.last_name}_{str(user_orm.id)[:4]}"
            )
            # First create the user in the firebase auth
            response = auth.create_user(
                email=data.email,
                display_name=display_name,
                uid=str(user_orm.id),
                password=data.password,
            )
            user = await self.udb.create_user(data=user_orm)
            assert user

            # Add role to user
            if role:
                r = await self.rm.get_role(role)
                if not r:
                    logger.error("failed to add user role")
                    return user
                user.roles.append(r)
                logger.debug("Added role succesfully")

            return user
        except Exception as e:
            raise ValueError(f"[UserManager] Failed to create user {e}")

    async def get_user(self, id: ID) -> User | None:
        """Fetches the users data

        Args:
            id (ID): _description_

        Returns:
            User|None: _description_
        """
        return await self.get_user(id)
