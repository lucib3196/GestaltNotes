"""Preview or apply course enrollments from a file of student emails."""

import argparse
from collections import Counter
from pathlib import Path
from uuid import UUID

from pydantic import EmailStr, TypeAdapter, ValidationError
from sqlalchemy import func
from sqlmodel import Session, select

from backend.accounts.models import User, UserRole
from backend.courses.models import Course, CourseEnrollment


def read_emails(path: Path) -> tuple[list[str], Counter[str]]:
    """Validate and deduplicate email addresses, preserving input order."""
    validator = TypeAdapter(EmailStr)
    counts: Counter[str] = Counter()
    emails: list[str] = []
    seen: set[str] = set()

    for number, line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        try:
            email = str(validator.validate_python(value)).lower()
        except ValidationError:
            print(f"INVALID line {number}: {value}")
            counts["invalid"] += 1
            continue
        if email in seen:
            counts["duplicates"] += 1
            continue
        seen.add(email)
        emails.append(email)

    return emails, counts


def run(session: Session, course_id: UUID, path: Path, *, apply: bool) -> int:
    """Build an enrollment preview and optionally commit new enrollments."""
    emails, counts = read_emails(path)
    course = session.get(Course, course_id)
    if course is None:
        raise ValueError(f"Course not found: {course_id}")
    professor = session.get(User, course.owner_id)
    if professor is None:
        raise ValueError("The course owner could not be found")
    professor_name = " ".join(
        part for part in (professor.first_name, professor.last_name) if part
    )
    professor_name = professor_name or professor.username or "Unnamed professor"

    print(f"\nMode: {'APPLY' if apply else 'DRY RUN'}")
    print(f"File: {path.resolve()}")
    print(f"Course: {course.name}")
    print(f"Course ID: {course.id}")
    print(f"Professor: {professor_name} <{professor.email}>")
    print(f"Description: {course.description or 'No description'}")
    print()
    pending: list[User] = []
    for email in emails:
        matches = session.exec(
            select(User).where(func.lower(User.email) == email)
        ).all()
        if not matches:
            print(f"NOT FOUND: {email}")
            counts["not_found"] += 1
            continue
        if len(matches) != 1:
            print(f"AMBIGUOUS MATCH: {email}")
            counts["ambiguous"] += 1
            continue
        student = matches[0]
        if not any(role.name == UserRole.STUDENT for role in student.roles):
            print(f"NOT A STUDENT: {email}")
            counts["not_student"] += 1
            continue
        enrollment = session.get(CourseEnrollment, (student.id, course.id))
        if enrollment is not None:
            label = "already_enrolled" if enrollment.active else "inactive"
            counts[label] += 1
            print(f"{label.replace('_', ' ').upper()}: {email}")
            continue
        pending.append(student)
        print(f"WOULD ENROLL: {email}")
    print(f"\nMode: {'APPLY' if apply else 'DRY RUN'}")
    print(f"File: {path.resolve()}")
    print(f"Course: {course.name}")
    print(f"Course ID: {course.id}")
    print(f"Professor: {professor_name} <{professor.email}>")
    print(f"Description: {course.description or 'No description'}")
    print()
    print(f"\nSummary: adding {len(pending)} students to {course.name}")
    for label in (
        "already_enrolled",
        "inactive",
        "duplicates",
        "invalid",
        "not_found",
        "ambiguous",
        "not_student",
    ):
        print(f"  {label.replace('_', ' ')}: {counts[label]}")
    blocked = any(
        counts[label] for label in ("invalid", "not_found", "ambiguous", "not_student")
    )
    if blocked:
        print("\nResolve the reported errors before applying. No changes made.")
        return 1
    if not apply:
        print("\nDry run complete. No changes made. Use --apply to enroll.")
        return 0
    if not pending:
        print("\nNo new enrollments needed.")
        return 0
    try:
        session.add_all(
            [
                CourseEnrollment(student_id=student.id, course_id=course.id)
                for student in pending
            ]
        )
        session.commit()
    except Exception:
        session.rollback()
        raise
    print(f"\nEnrolled {len(pending)} students in {course.name}.")
    return 0


def main() -> int:
    """Read CLI arguments and run against the configured application database."""
    parser = argparse.ArgumentParser(
        description="Preview or apply course enrollments from an email file."
    )
    parser.add_argument("file", type=Path)
    parser.add_argument("--course-id", type=UUID, required=True)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Commit enrollments; otherwise perform a read-only dry run.",
    )
    args = parser.parse_args()
    # Register all database models before querying related tables.
    import backend.database.models  # noqa: F401
    from backend.database.config import open_session

    try:
        with open_session() as session:
            return run(session, args.course_id, args.file, apply=args.apply)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
