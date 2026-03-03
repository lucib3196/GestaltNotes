from src.data.user import UserDB
from src.model.user import User, UserCreate
from firebase_admin import auth
from sqlmodel import Session
from src.model.user import User, UserCreate, VALID_ROLES
from src.data.role import RoleDB
from . import ID, logger


class UserManager:
    def __init__(self, session: Session):
        self.udb = UserDB(session)
        self.rm = RoleDB(session)

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
            user = await self.udb.create_user(data=user_orm)
            assert user
            display_name = f"{user_orm.email.split("@")[0]}_{str(user_orm.id)[:4]}"
            # First create the user in the firebase auth
            response = auth.create_user(
                email=data.email,
                display_name=display_name,
                uid=str(user.id),
                password=data.password,
            )
            # Add role to user
            if role:
                r = await self.rm.get_role(role)
                if not r:
                    logger.error("failed to add user role")
                    return user
                user.roles.append(r)
                logger.debug("Added role succesfully")

            if force_password_reset:
                auth.set_custom_user_claims(
                    str(user.id), {"force_password_reset": True}
                )

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
        return await self.udb.get_user(id)
