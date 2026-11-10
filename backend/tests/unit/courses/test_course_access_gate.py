import pytest
from authorization import AccessDeniedError, RoleAccessDeniedError

from backend.accounts.models import Role, User, UserRole
from backend.courses.models import Course, CourseEnrollment
from backend.courses.service.course_access_gate import (
    CourseAccessGate,
    CourseOwnershipAccessGate,
)


def test_course_access_requires_active_enrollment(db_session):
    educator = User(email="educator@example.com")
    student = User(email="student@example.com")
    outsider = User(email="outsider@example.com")
    course = Course(name="Course", owner_id=educator.id)
    enrollment = CourseEnrollment(student_id=student.id, course_id=course.id)
    db_session.add_all([educator, student, outsider, course])
    db_session.flush()
    db_session.add(enrollment)
    db_session.flush()

    gate = CourseAccessGate(db_session)
    assert gate.require_access(student, course).access
    with pytest.raises(AccessDeniedError):
        gate.require_access(outsider, course)

    enrollment.active = False
    db_session.flush()
    with pytest.raises(AccessDeniedError):
        gate.require_access(student, course)


def test_course_ownership():
    owner = User(email="owner@example.com")
    outsider = User(email="outsider@example.com")
    course = Course(name="Course", owner_id=owner.id)
    gate = CourseOwnershipAccessGate()

    assert gate.require_access(owner, course).access
    assert gate.require_ownership(owner, course).access
    with pytest.raises(AccessDeniedError):
        gate.require_access(outsider, course)
    with pytest.raises(AccessDeniedError):
        gate.require_ownership(outsider, course)


def test_course_roles(db_session):
    student = User(
        email="student@example.com",
        roles=[Role(name=UserRole.STUDENT)],
    )
    gate = CourseAccessGate(db_session)

    assert gate.require_roles(student, [UserRole.STUDENT]).access
    with pytest.raises(RoleAccessDeniedError):
        gate.require_roles(student, [UserRole.EDUCATOR])
