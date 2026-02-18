from src.model.user import Role, VALID_ROLES
import asyncio
from typing import Literal, List
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from . import ID, logger


class RoleDB:
    def __init__(self, session: Session):
        self.session = session

    async def create_role(self, name: VALID_ROLES) -> Role:
        try:
            role_orm = Role(name=name)
            self.session.add(role_orm)
            self.session.commit()
            self.session.flush()
            return role_orm
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ROLEDB] Failed to create role {e}"
            logger.error(message)
            raise ValueError(message)

    async def get_role(self, name: VALID_ROLES) -> Role:
        try:
            stmt = select(Role).where(Role.name == name)
            role = self.session.exec(stmt).first()
            if not role:
                raise ValueError(f"[ROLEDB] Fole {name} does not exist in DB")
            return role
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ROLEDB] Failed to get role {e}"
            logger.error(message)
            raise ValueError(message)

    async def seed_roles(self) -> List[Role]:
        roles: List[VALID_ROLES] = ["educator", "student", "admin"]
        return await asyncio.gather(*[self.create_role(r) for r in roles])
