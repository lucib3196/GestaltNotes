from sqlmodel import Session
from src.model.user import User, UserCreate, VALID_ROLES
from src.service.user.user_manager import UserManager
from src.data.role import RoleDB


class EducatorServer:
    def __init__(self, session: Session):
        self.um = UserManager(session)

    async def create_account(self, data: UserCreate) -> User:
        return await self.um.create_user(data, role="educator")
