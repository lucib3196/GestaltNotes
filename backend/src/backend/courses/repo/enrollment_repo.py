from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select

from backend.courses.exceptions import CourseEnrollmentNotFoundError
from backend.courses.models import CourseEnrollment, CourseEnrollmentUpdate


class EnrollmentRepo:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def create(self, record: CourseEnrollment) -> CourseEnrollment:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    async def get(
        self,
        student_id: UUID,
        course_id: UUID,
    ) -> CourseEnrollment | None:
        return self._session.get(
            CourseEnrollment,
            (student_id, course_id),
        )

    async def update(
        self,
        record: CourseEnrollment,
        update: CourseEnrollmentUpdate,
    ) -> CourseEnrollment:
        if (
            update.student_id != record.student_id
            or update.course_id != record.course_id
        ):
            raise ValueError("Enrollment IDs cannot be changed")

        record.active = update.active
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    async def update_by_id(
        self,
        student_id: UUID,
        course_id: UUID,
        update: CourseEnrollmentUpdate,
    ) -> CourseEnrollment:
        record = await self.get(student_id, course_id)
        if record is None:
            raise CourseEnrollmentNotFoundError(
                f"Student '{student_id}' is not enrolled in course '{course_id}'"
            )
        return await self.update(record, update)

    async def delete(self, student_id: UUID, course_id: UUID) -> None:
        record = await self.get(student_id, course_id)
        if record is not None:
            self._session.delete(record)
            self._session.flush()

    async def list(self) -> Sequence[CourseEnrollment]:
        return self._session.exec(select(CourseEnrollment)).all()

    async def list_by_student(
        self,
        student_id: UUID,
    ) -> Sequence[CourseEnrollment]:
        return self._session.exec(
            select(CourseEnrollment).where(CourseEnrollment.student_id == student_id)
        ).all()

    async def list_by_course(
        self,
        course_id: UUID,
    ) -> Sequence[CourseEnrollment]:
        return self._session.exec(
            select(CourseEnrollment).where(CourseEnrollment.course_id == course_id)
        ).all()
