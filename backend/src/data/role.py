from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from src.model.user import VALID_ROLES, Role

from . import logger


class RoleDB:
    def __init__(self, session: Session) -> None:
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

    async def get_role(self, name: VALID_ROLES) -> Role | None:
        try:
            stmt = select(Role).where(Role.name == name)
            return self.session.exec(stmt).first()
        except SQLAlchemyError as e:
            self.session.rollback()
            message = f"[ROLEDB] Failed to get role {e}"
            logger.error(message)
            raise ValueError(message)

    async def seed_roles(self) -> list[Role]:
        roles: list[VALID_ROLES] = ["educator", "student", "admin"]
        created_roles = []
        for r in roles:
            r_exist = await self.get_role(r)
            if r_exist:
                created_roles.append(r_exist)
            else:
                created_roles.append(await self.create_role(r))
        return created_roles
