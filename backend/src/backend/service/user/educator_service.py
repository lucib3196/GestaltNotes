from sqlmodel import Session

from src.model.user import User, UserCreate
from src.service.user.user_manager import UserManager


class EducatorServer:
    def __init__(self, session: Session) -> None:
        self.um = UserManager(session)

    async def create_account(self, data: UserCreate) -> User:
        return await self.um.create_user(data, role="educator")
