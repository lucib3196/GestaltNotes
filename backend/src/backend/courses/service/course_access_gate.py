from collections.abc import Iterable

from authorization import AccessGate, OwnershipAccessGate
from authorization.service import AccessDecision
from sqlmodel import Session, col, select

from backend.accounts.models import Role, User, UserRole
from backend.courses.models import Course, CourseEnrollment


class CourseAccessGate(AccessGate[UserRole, Course, User]):
    """Allow course access for actively enrolled students."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def check_access(self, actor: User, resource: Course) -> AccessDecision:
        """Check for an active enrollment in the supplied course."""
        stmt = select(CourseEnrollment).where(
            col(CourseEnrollment.student_id) == actor.id,
            col(CourseEnrollment.course_id) == resource.id,
            col(CourseEnrollment.active).is_(True),
        )
        enrollment = self._session.exec(stmt).first()
        if not enrollment:
            return AccessDecision(
                access=False, message="Active course enrollment required"
            )
        return AccessDecision(access=True, message="Active course enrollment confirmed")

    def get_roles(self, actor: User) -> Iterable[UserRole]:
        """Extract role values from the user's role records."""
        return [role.name for role in actor.roles]


class CourseOwnershipAccessGate(OwnershipAccessGate[UserRole, Course, User]):
    """Allow course access for its owner."""

    def check_ownership(self, actor: User, resource: Course) -> AccessDecision:
        """Check whether the actor owns the supplied course."""
        if resource.owner_id != actor.id:
            return AccessDecision(access=False, message="Course ownership required")
        return AccessDecision(access=True, message="Course ownership confirmed")

    def check_access(self, actor: User, resource: Course) -> AccessDecision:
        """Require ownership for access through this gate."""
        return self.check_ownership(actor, resource)

    def get_roles(self, actor: User) -> Iterable[UserRole]:
        """Extract role values from the user's role records."""
        return [role.name for role in actor.roles]
