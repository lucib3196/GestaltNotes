from fastapi.routing import APIRouter
from sqlmodel import select

from backend.accounts.models import Role, User, UserRole, UserRoleLink
from backend.accounts.schema import StudentResponse
from backend.database import SessionDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/students", response_model=list[StudentResponse])
def get_students(session: SessionDep) -> list[User]:
    return session.exec(
        select(User)
        .join(UserRoleLink, UserRoleLink.user_id == User.id)
        .join(Role, Role.id == UserRoleLink.role_id)
        .where(Role.name == UserRole.STUDENT)
    ).all()
