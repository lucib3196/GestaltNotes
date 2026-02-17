from src.model.user import User, UserCreate
from sqlmodel import Session, select
from src.core.logger import logger

from sqlalchemy.exc import SQLAlchemyError
from . import ID


class UserDB:
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, data: UserCreate | User) -> User | None:
        try:
            user_orm = User(
                first_name=data.first_name, last_name=data.last_name, email=data.email
            )
            self.session.add(user_orm)
            self.session.commit()
            self.session.flush()
            return user_orm
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[UserDB] failed to create user {e}"
            logger.error(message)
            raise ValueError(message)

    async def get_user(self, id: ID) -> User | None:
        try:
            return self.session.exec(select(User).where(User.id == ID)).first()
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[UserDB] failed to get user {e}"
            logger.error(message)
            raise ValueError(message)
