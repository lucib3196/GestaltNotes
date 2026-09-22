from datetime import datetime
from hashlib import sha256
from secrets import choice
from string import ascii_uppercase, digits

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from backend.accounts.models import User
from backend.core import logger
from backend.courses.exceptions import (
    CourseAccessCodeCreationError,
    CourseAccessCodeDisabledError,
    CourseAccessCodeExpiredError,
    CourseAccessCodeInvalidError,
    CourseAccessCodeNotFoundError,
    CourseAccessCodeRetrievalError,
    CourseEnrollmentAlreadyExistsError,
    CourseEnrollmentError,
)
from backend.courses.models import CourseAccessCode, CourseEnrollment
from backend.courses.service.course_service import CourseService
from backend.courses.service.enrollment_service import CourseEnrollmentService
from backend.shared.types import ID
from backend.utils.utils import convert_uuid


class CourseAccessCodeService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._course_service = CourseService(session)
        self._enrollment_service = CourseEnrollmentService(session)

    async def create_access_code(
        self,
        course_id: ID,
        educator: User,
        expires_at: datetime | None = None,
    ) -> str:
        await self._course_service.assert_course_owner(course_id, educator)

        code = self._generate_code()
        code_hash = self._hash_code(code)

        try:
            access_code = CourseAccessCode(
                course_id=convert_uuid(course_id),
                code_hash=code_hash,
                expires_at=expires_at,
            )
            self._session.add(access_code)
            self._session.commit()
            self._session.refresh(access_code)
            return code
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseAccessCodeService] failed to create access code {e}"
            logger.error(message)
            raise CourseAccessCodeCreationError(message) from e

    async def rotate_access_code(
        self,
        course_id: ID,
        educator: User,
        expires_at: datetime | None = None,
    ) -> str:
        await self.disable_active_codes(course_id, educator)
        return await self.create_access_code(course_id, educator, expires_at)

    async def disable_active_codes(self, course_id: ID, educator: User) -> None:
        await self._course_service.assert_course_owner(course_id, educator)

        try:
            codes = self._session.exec(
                select(CourseAccessCode).where(
                    CourseAccessCode.course_id == convert_uuid(course_id),
                    CourseAccessCode.active == True,
                )
            ).all()

            for code in codes:
                code.active = False
                self._session.add(code)

            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseAccessCodeService] failed to disable access codes {e}"
            logger.error(message)
            raise CourseAccessCodeCreationError(message) from e

    async def validate_access_code(self, code: str) -> CourseAccessCode:
        normalized_code = self._normalize_code(code)

        try:
            access_code = self._session.exec(
                select(CourseAccessCode).where(
                    CourseAccessCode.code_hash == self._hash_code(normalized_code)
                )
            ).first()
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseAccessCodeService] failed to retrieve access code {e}"
            logger.error(message)
            raise CourseAccessCodeRetrievalError(message) from e

        if not access_code:
            raise CourseAccessCodeNotFoundError("Access code not found")

        if not access_code.active:
            raise CourseAccessCodeDisabledError("Access code is disabled")

        if access_code.expires_at and access_code.expires_at < datetime.utcnow():
            raise CourseAccessCodeExpiredError("Access code is expired")

        return access_code

    async def redeem_access_code(self, code: str, student: User) -> CourseEnrollment:
        access_code = await self.validate_access_code(code)

        try:
            enrollment = await self._enrollment_service.enroll_student(
                access_code.course_id,
                student,
            )
            access_code.uses += 1
            self._session.add(access_code)
            self._session.commit()
            self._session.refresh(enrollment)
            return enrollment
        except CourseEnrollmentAlreadyExistsError:
            raise
        except SQLAlchemyError as e:
            self._session.rollback()
            message = f"[CourseAccessCodeService] failed to redeem access code {e}"
            logger.error(message)
            raise CourseEnrollmentError(message) from e

    def _generate_code(self) -> str:
        alphabet = ascii_uppercase + digits
        parts = ["".join(choice(alphabet) for _ in range(4)) for _ in range(3)]
        return "-".join(parts)

    def _normalize_code(self, code: str) -> str:
        normalized = code.strip().upper()
        if not normalized:
            raise CourseAccessCodeInvalidError("Access code cannot be empty")
        return normalized

    def _hash_code(self, code: str) -> str:
        return sha256(self._normalize_code(code).encode("utf-8")).hexdigest()
