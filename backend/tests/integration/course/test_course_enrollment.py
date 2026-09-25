from uuid import uuid4

import pytest

from backend.accounts.models import UserRole
from backend.courses.exceptions import (
    CourseEnrollmentAlreadyExistsError,
    CourseEnrollmentNotFoundError,
    CourseEnrollmentPermissionError,
    CourseOwnershipError,
)


def unique_user_fields(prefix: str) -> dict[str, str]:
    suffix = uuid4().hex
    return {
        "email": f"{prefix}-{suffix}@example.com",
        "username": f"{prefix}-{suffix}",
    }


@pytest.mark.asyncio
async def test_enroll_student(enrollment_service, make_user, make_course):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None
    assert student.id is not None

    enrollment = await enrollment_service.enroll_student(course.id, student)

    assert enrollment.course_id == course.id
    assert enrollment.student_id == student.id
    assert enrollment.active is True


@pytest.mark.asyncio
async def test_enroll_student_rejects_non_student(
    enrollment_service,
    make_user,
    make_course,
):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    course = await make_course(educator)
    assert course.id is not None

    with pytest.raises(CourseEnrollmentPermissionError):
        await enrollment_service.enroll_student(course.id, educator)


@pytest.mark.asyncio
async def test_enroll_student_rejects_duplicate_enrollment(
    enrollment_service,
    make_user,
    make_course,
):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None

    await enrollment_service.enroll_student(course.id, student)

    with pytest.raises(CourseEnrollmentAlreadyExistsError):
        await enrollment_service.enroll_student(course.id, student)


@pytest.mark.asyncio
async def test_educator_can_enroll_student(
    enrollment_service,
    make_user,
    make_course,
):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None
    assert student.id is not None

    enrollment = await enrollment_service.enroll_student_by_educator(
        course.id,
        student,
        educator,
    )

    assert enrollment.course_id == course.id
    assert enrollment.student_id == student.id


@pytest.mark.asyncio
async def test_non_owner_cannot_enroll_student(
    enrollment_service,
    make_user,
    make_course,
):
    owner = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("owner"),
    )
    other_educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("other-educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(owner)
    assert course.id is not None

    with pytest.raises(CourseOwnershipError):
        await enrollment_service.enroll_student_by_educator(
            course.id,
            student,
            other_educator,
        )


@pytest.mark.asyncio
async def test_educator_can_enroll_student_by_id(
    enrollment_service,
    make_user,
    make_course,
):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None
    assert student.id is not None

    enrollment = await enrollment_service.enroll_student_by_id_by_educator(
        course.id,
        student.id,
        educator,
    )

    assert enrollment.course_id == course.id
    assert enrollment.student_id == student.id


@pytest.mark.asyncio
async def test_get_enrollment(enrollment_service, make_user, make_course):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None
    assert student.id is not None

    created = await enrollment_service.enroll_student(course.id, student)

    found = await enrollment_service.get_enrollment(course.id, student.id)

    assert found.course_id == created.course_id
    assert found.student_id == created.student_id


@pytest.mark.asyncio
async def test_get_enrollment_raises_when_missing(
    enrollment_service,
    make_user,
    make_course,
):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None
    assert student.id is not None

    with pytest.raises(CourseEnrollmentNotFoundError):
        await enrollment_service.get_enrollment(course.id, student.id)


@pytest.mark.asyncio
async def test_list_students(enrollment_service, make_user, make_course):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    first_student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("first-student"),
    )
    second_student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("second-student"),
    )
    course = await make_course(educator)
    assert course.id is not None

    await enrollment_service.enroll_student(course.id, first_student)
    await enrollment_service.enroll_student(course.id, second_student)

    students = await enrollment_service.list_students(course.id, educator)

    assert {student.id for student in students} == {
        first_student.id,
        second_student.id,
    }


@pytest.mark.asyncio
async def test_list_student_courses(enrollment_service, make_user, make_course):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    first_course = await make_course(educator, name="Mechanics")
    second_course = await make_course(educator, name="Thermodynamics")
    assert first_course.id is not None
    assert second_course.id is not None

    await enrollment_service.enroll_student(first_course.id, student)
    await enrollment_service.enroll_student(second_course.id, student)

    courses = await enrollment_service.list_student_courses(student)

    assert {course.id for course in courses} == {first_course.id, second_course.id}


@pytest.mark.asyncio
async def test_unenroll_student(enrollment_service, make_user, make_course):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None
    assert student.id is not None

    await enrollment_service.enroll_student(course.id, student)

    await enrollment_service.unenroll_student(course.id, student.id, educator)

    with pytest.raises(CourseEnrollmentNotFoundError):
        await enrollment_service.get_enrollment(course.id, student.id)


@pytest.mark.asyncio
async def test_non_owner_cannot_unenroll_student(
    enrollment_service,
    make_user,
    make_course,
):
    owner = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("owner"),
    )
    other_educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("other-educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(owner)
    assert course.id is not None
    assert student.id is not None

    await enrollment_service.enroll_student(course.id, student)

    with pytest.raises(CourseOwnershipError):
        await enrollment_service.unenroll_student(
            course.id,
            student.id,
            other_educator,
        )


@pytest.mark.asyncio
async def test_is_enrolled(enrollment_service, make_user, make_course):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None

    assert await enrollment_service.is_enrolled(course.id, student) is False

    await enrollment_service.enroll_student(course.id, student)

    assert await enrollment_service.is_enrolled(course.id, student) is True


@pytest.mark.asyncio
async def test_assert_course_access_allows_owner_and_enrolled_student(
    enrollment_service,
    make_user,
    make_course,
):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None

    owner_course = await enrollment_service.assert_course_access(course.id, educator)

    await enrollment_service.enroll_student(course.id, student)
    student_course = await enrollment_service.assert_course_access(course.id, student)

    assert owner_course.id == course.id
    assert student_course.id == course.id


@pytest.mark.asyncio
async def test_assert_course_access_rejects_unenrolled_student(
    enrollment_service,
    make_user,
    make_course,
):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )
    course = await make_course(educator)
    assert course.id is not None

    with pytest.raises(CourseEnrollmentPermissionError):
        await enrollment_service.assert_course_access(course.id, student)
