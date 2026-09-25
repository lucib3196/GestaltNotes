from uuid import uuid4

import pytest

from backend.accounts.models import UserRole
from backend.courses import CourseCreate
from backend.courses.exceptions import (
    CourseNotFoundError,
    CourseOwnershipError,
    CoursePermissionError,
)
from backend.courses.schema import CourseUpdate
from backend.courses.service.course_service import CourseService


def unique_user_fields(prefix: str) -> dict[str, str]:
    suffix = uuid4().hex
    return {
        "email": f"{prefix}-{suffix}@example.com",
        "username": f"{prefix}-{suffix}",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("account_service", ["fake", "real"], indirect=True)
async def test_create_course(course_service: CourseService, make_user):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    course = await course_service.create_course(
        data=CourseCreate(
            name="Mechanics",
            discipline="Physics",
            description="Intro mechanics",
        ),
        educator=educator,
    )

    assert course.id is not None
    assert course.name == "Mechanics"
    assert course.discipline == "Physics"
    assert course.description == "Intro mechanics"
    assert course.storage_prefix == f"courses/{course.id}"
    assert course.owner_id == educator.id


@pytest.mark.asyncio
@pytest.mark.parametrize("account_service", ["fake", "real"], indirect=True)
async def test_get_course(course_service: CourseService, make_user):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    course = await course_service.create_course(
        data=CourseCreate(name="Mechanics"),
        educator=educator,
    )
    assert course.id

    found_course = await course_service.get_course(course.id)

    assert found_course.id == course.id
    assert found_course.name == "Mechanics"
    assert found_course.owner_id == educator.id


@pytest.mark.asyncio
@pytest.mark.parametrize("account_service", ["fake", "real"], indirect=True)
async def test_list_owned_courses(course_service: CourseService, make_user):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    first_course = await course_service.create_course(
        data=CourseCreate(name="Mechanics"),
        educator=educator,
    )
    second_course = await course_service.create_course(
        data=CourseCreate(name="Thermodynamics"),
        educator=educator,
    )

    courses = await course_service.list_owned_courses(educator)

    assert {course.id for course in courses} == {first_course.id, second_course.id}


@pytest.mark.asyncio
@pytest.mark.parametrize("account_service", ["fake", "real"], indirect=True)
async def test_update_course(course_service: CourseService, make_user):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    course = await course_service.create_course(
        data=CourseCreate(name="Mechanics"),
        educator=educator,
    )
    assert course.id
    updated_course = await course_service.update_course(
        course.id,
        CourseUpdate(
            name="Advanced Mechanics",
            discipline="Physics",
            description="Updated course",
        ),
        educator=educator,
    )

    assert updated_course.id == course.id
    assert updated_course.name == "Advanced Mechanics"
    assert updated_course.discipline == "Physics"
    assert updated_course.description == "Updated course"
    assert updated_course.storage_prefix == f"courses/{course.id}"


@pytest.mark.asyncio
@pytest.mark.parametrize("account_service", ["fake", "real"], indirect=True)
async def test_delete_course(course_service: CourseService, make_user):
    educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("educator"),
    )
    course = await course_service.create_course(
        data=CourseCreate(name="Mechanics"),
        educator=educator,
    )
    assert course.id
    result = await course_service.delete_course(course.id, educator)
    assert course.id
    assert result.success is True
    with pytest.raises(CourseNotFoundError):
        await course_service.get_course(course.id)


@pytest.mark.asyncio
@pytest.mark.parametrize("account_service", ["fake", "real"], indirect=True)
async def test_student_cannot_create_course(course_service: CourseService, make_user):
    student = await make_user(
        role=UserRole.STUDENT,
        **unique_user_fields("student"),
    )

    with pytest.raises(CoursePermissionError):
        await course_service.create_course(
            data=CourseCreate(name="Mechanics"),
            educator=student,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("account_service", ["fake", "real"], indirect=True)
async def test_non_owner_cannot_update_course(course_service: CourseService, make_user):
    owner = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("owner"),
    )
    other_educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("other-educator"),
    )
    course = await course_service.create_course(
        data=CourseCreate(name="Mechanics"),
        educator=owner,
    )
    assert course.id

    with pytest.raises(CourseOwnershipError):
        await course_service.update_course(
            course.id,
            CourseUpdate(name="Stolen Mechanics"),
            other_educator,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("account_service", ["fake", "real"], indirect=True)
async def test_non_owner_cannot_delete_course(course_service: CourseService, make_user):
    owner = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("owner"),
    )
    other_educator = await make_user(
        role=UserRole.EDUCATOR,
        **unique_user_fields("other-educator"),
    )
    course = await course_service.create_course(
        data=CourseCreate(name="Mechanics"),
        educator=owner,
    )

    with pytest.raises(CourseOwnershipError):
        assert course.id
        await course_service.delete_course(course.id, other_educator)
