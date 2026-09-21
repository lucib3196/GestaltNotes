from sqlmodel import Session

from backend.model.user import User, UserCreate
from backend.service.user.user_manager import UserManager


class EducatorServer:
    def __init__(self, session: Session) -> None:
        self.um = UserManager(session)

    async def create_account(self, data: UserCreate) -> User:
        return await self.um.create_user(data, role="educator")
