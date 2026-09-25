from backend.service.user.user_manager import UserManager
from sqlmodel import Session

from backend.accounts.models import User
from backend.accounts.schema import UserCreate


class EducatorServer:
    def __init__(self, session: Session) -> None:
        self.um = UserManager(session)

    async def create_account(self, data: UserCreate) -> User:
        return await self.um.create_user(data, role="educator")
