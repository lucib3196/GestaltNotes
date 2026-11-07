from unittest.mock import patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select

import backend.database.models  # noqa: F401
from backend.accounts.models import Role, User, UserRole
from backend.batch.enroll_students import read_emails, run
from backend.courses.models import Course, CourseEnrollment


@pytest.fixture
def enrollment_data(db_session, tmp_path):
    student_role = db_session.exec(
        select(Role).where(Role.name == UserRole.STUDENT)
    ).one()
    professor = User(
        email="professor@example.com", first_name="Ada", last_name="Lovelace"
    )
    students = [
        User(email=f"student{number}@example.com", roles=[student_role])
        for number in range(2)
    ]
    db_session.add_all([professor, *students])
    db_session.flush()
    course = Course(
        name="Mechanics", owner_id=professor.id, description="Introductory mechanics"
    )
    db_session.add(course)
    db_session.commit()
    path = tmp_path / "emails.txt"
    path.write_text("\n".join(str(student.email) for student in students))
    return course, students, path


def test_read_emails_validates_and_deduplicates(tmp_path):
    path = tmp_path / "emails.txt"
    path.write_text(
        "\ufeff# Student list\n\n Student@EXAMPLE.COM \nstudent@example.com\ninvalid\n",
        encoding="utf-8",
    )
    emails, counts = read_emails(path)
    assert emails == ["student@example.com"]
    assert counts["duplicates"] == 1
    assert counts["invalid"] == 1


def test_dry_run_reports_course_without_writes(db_session, enrollment_data, capsys):
    course, _, path = enrollment_data
    with patch.object(db_session, "commit", wraps=db_session.commit) as commit:
        assert run(db_session, course.id, path, apply=False) == 0
        commit.assert_not_called()
    assert db_session.exec(select(CourseEnrollment)).all() == []
    output = capsys.readouterr().out
    assert "Course: Mechanics" in output
    assert "Professor: Ada Lovelace <professor@example.com>" in output
    assert "adding 2 students" in output


def test_apply_enrolls_and_rerun_skips_existing(db_session, enrollment_data):
    course, students, path = enrollment_data
    assert run(db_session, course.id, path, apply=True) == 0
    assert run(db_session, course.id, path, apply=True) == 0
    enrolled = db_session.exec(select(CourseEnrollment)).all()
    assert {row.student_id for row in enrolled} == {student.id for student in students}
    assert all(row.course_id == course.id and row.active for row in enrolled)


@pytest.mark.parametrize(
    "extra_email", ["missing@example.com", "invalid", "professor@example.com"]
)
def test_errors_block_entire_apply(db_session, enrollment_data, extra_email):
    course, _, path = enrollment_data
    path.write_text(path.read_text() + "\n" + extra_email)
    assert run(db_session, course.id, path, apply=True) == 1
    assert db_session.exec(select(CourseEnrollment)).all() == []


def test_inactive_enrollment_is_not_reactivated(db_session, enrollment_data):
    course, students, path = enrollment_data
    db_session.add(
        CourseEnrollment(student_id=students[0].id, course_id=course.id, active=False)
    )
    db_session.commit()
    assert run(db_session, course.id, path, apply=True) == 0
    rows = db_session.exec(select(CourseEnrollment)).all()
    assert len(rows) == 2
    assert not next(row for row in rows if row.student_id == students[0].id).active


def test_ambiguous_case_insensitive_email_blocks_apply(db_session, enrollment_data):
    course, _, path = enrollment_data
    db_session.add(User(email="STUDENT0@example.com"))
    db_session.commit()
    assert run(db_session, course.id, path, apply=True) == 1
    assert db_session.exec(select(CourseEnrollment)).all() == []


def test_missing_course_fails(db_session, enrollment_data):
    _, _, path = enrollment_data
    with pytest.raises(ValueError, match="Course not found"):
        run(db_session, uuid4(), path, apply=True)


def test_failed_apply_rolls_back_all_enrollments(db_session, enrollment_data):
    course, _, path = enrollment_data

    def fail_commit():
        db_session.flush()
        raise SQLAlchemyError("Commit failed")

    with (
        patch.object(db_session, "commit", side_effect=fail_commit),
        pytest.raises(SQLAlchemyError, match="Commit failed"),
    ):
        run(db_session, course.id, path, apply=True)
    assert db_session.exec(select(CourseEnrollment)).all() == []
