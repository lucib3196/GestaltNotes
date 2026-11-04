from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session

from backend.accounts.models import User, UserRole
from backend.core import logger
from backend.courses.exceptions import (
    CourseEnrollmentAlreadyExistsError,
    CourseEnrollmentCreationError,
    CourseEnrollmentDeletionError,
    CourseEnrollmentNotFoundError,
    CourseEnrollmentPermissionError,
    CourseEnrollmentRetrievalError,
    CourseNotFoundError,
)
from backend.courses.models import Course, CourseEnrollment
from backend.courses.repo import CourseRepo, EnrollmentRepo
from backend.courses.service.course_access_service import CourseAccess


class CourseEnrollmentService:
    def __init__(self, session: Session) -> None:

        self._session = session
        self._courses = CourseRepo(session)
        self._enrollments = EnrollmentRepo(session)
        self._access = CourseAccess(self._courses)

    async def enroll_student(self, course_id: UUID, student: User) -> CourseEnrollment:
        self._assert_student(student)

        if not student.id:
            raise CourseEnrollmentCreationError("Cannot enroll user without id")

        course = await self._courses.get(course_id)
        if not course:
            raise CourseEnrollmentCreationError(
                "Cannot enroll in course. Course does not exist"
            )

        try:
            enrollment = await self._enrollments.create(
                CourseEnrollment(student_id=student.id, course_id=course.id)
            )
            self._session.commit()
            return enrollment
        except IntegrityError as e:
            self._session.rollback()
            message = (
                f"[CourseEnrollmentService] student '{student.id}' is already "
                f"enrolled in course '{course_id}'"
            )
            logger.error(message)
            raise CourseEnrollmentAlreadyExistsError(message) from e
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseEnrollmentService] failed to enroll student {e}"
            logger.error(message)
            raise CourseEnrollmentCreationError(message) from e

    async def enroll_student_by_educator(
        self,
        course_id: UUID,
        student: User,
        educator: User,
    ) -> CourseEnrollment:
        await self._access.require_owner(course_id, educator)
        return await self.enroll_student(course_id, student)

    async def enroll_student_by_id_by_educator(
        self,
        course_id: UUID,
        student_id: UUID,
        educator: User,
    ) -> CourseEnrollment:
        course = await self._access.require_owner(course_id, educator)
        if not course.id:
            raise CourseEnrollmentCreationError("Cannot enroll in course without id")

        try:
            enrollment = await self._enrollments.create(
                CourseEnrollment(student_id=student_id, course_id=course.id)
            )
            self._session.commit()
            return enrollment
        except IntegrityError as e:
            self._session.rollback()
            message = (
                f"[CourseEnrollmentService] student '{student_id}' is already "
                f"enrolled in course '{course_id}'"
            )
            logger.error(message)
            raise CourseEnrollmentAlreadyExistsError(message) from e
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseEnrollmentService] failed to enroll student {e}"
            logger.error(message)
            raise CourseEnrollmentCreationError(message) from e

    async def unenroll_student(
        self,
        course_id: UUID,
        student_id: UUID,
        educator: User,
    ) -> None:
        await self._access.require_owner(course_id, educator)
        enrollment = await self.get_enrollment(course_id, student_id)

        try:
            await self._enrollments.delete(
                student_id=enrollment.student_id, course_id=enrollment.course_id
            )
            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseEnrollmentService] failed to unenroll student {e}"
            logger.error(message)
            raise CourseEnrollmentDeletionError(message) from e

    async def get_enrollment(
        self, course_id: UUID, student_id: UUID
    ) -> CourseEnrollment:
        try:
            enrollment = await self._enrollments.get(
                student_id=student_id,
                course_id=course_id,
            )
            if not enrollment:
                raise CourseEnrollmentNotFoundError(
                    f"Student '{student_id}' is not enrolled in course '{course_id}'"
                )
            return enrollment
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseEnrollmentService] failed to retrieve enrollment {e}"
            logger.error(message)
            raise CourseEnrollmentRetrievalError(message) from e

    async def list_students(self, course_id: UUID, educator: User) -> list[User]:
        course = await self._access.require_owner(course_id, educator)
        return list(course.students)

    async def list_student_courses(self, student: User) -> list[Course]:
        self._assert_student(student)
        return list(student.enrolled_courses)

    async def list_accessible_courses(self, user: User) -> list[Course]:
        courses: list[Course] = []

        if self._is_educator(user):
            courses.extend(user.owned_courses)

        if self._is_student(user):
            courses.extend(user.enrolled_courses)

        return list({course.id: course for course in courses}.values())

    async def is_enrolled(self, course_id: UUID, student: User) -> bool:
        if not student.id:
            return False

        try:
            await self.get_enrollment(course_id, student.id)
            return True
        except CourseEnrollmentNotFoundError:
            return False

    async def assert_course_access(self, course_id: UUID, user: User) -> Course:
        if self._is_educator(user):
            return await self._access.require_owner(course_id, user)

        if self._is_student(user):
            if await self.is_enrolled(course_id, user):
                course = await self._courses.get(course_id)
                if course is None:
                    raise CourseNotFoundError(str(course_id))
                return course
            raise CourseEnrollmentPermissionError(
                f"Student '{user.id}' is not enrolled in course '{course_id}'"
            )

        raise CourseEnrollmentPermissionError("Course access requires a valid role")

    def _assert_student(self, user: User) -> None:
        if not self._is_student(user):
            raise CourseEnrollmentPermissionError("Student role required")

    def _is_student(self, user: User) -> bool:
        return any(role.name == UserRole.STUDENT for role in user.roles)

    def _is_educator(self, user: User) -> bool:
        return any(role.name == UserRole.EDUCATOR for role in user.roles)
