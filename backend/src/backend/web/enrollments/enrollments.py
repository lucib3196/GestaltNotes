from uuid import UUID

from fastapi.routing import APIRouter
from pydantic import BaseModel
from starlette import status

from backend.accounts.models import User
from backend.courses.exceptions import CourseServiceException
from backend.courses.models import Course, CourseEnrollment, CourseVectorStore
from backend.courses.schema import CourseRead
from backend.web.accounts.dependencies import CurrentUserDep, EducatorDep, StudentDep
from backend.web.enrollments.dependencies import CourseEnrollmentServiceDep

from ..courses.http import course_http_exception

ID = UUID | str

router = APIRouter(prefix="/courses", tags=["course-enrollments"])


class CourseChatContext(BaseModel):
    course: Course
    vectorstore: CourseVectorStore | None


@router.post(
    "/{course_id}/enrollments/{student_id}",
    response_model=CourseEnrollment,
    status_code=status.HTTP_201_CREATED,
)
async def enroll_student_by_educator(
    enrollment_service: CourseEnrollmentServiceDep,
    educator: EducatorDep,
    course_id: ID,
    student_id: ID,
) -> CourseEnrollment:
    try:
        return await enrollment_service.enroll_student_by_id_by_educator(
            course_id,
            student_id,
            educator,
        )
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.delete(
    "/{course_id}/enrollments/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unenroll_student(
    enrollment_service: CourseEnrollmentServiceDep,
    educator: EducatorDep,
    course_id: ID,
    student_id: ID,
) -> None:
    try:
        await enrollment_service.unenroll_student(course_id, student_id, educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}/students", response_model=list[User])
async def list_students(
    enrollment_service: CourseEnrollmentServiceDep,
    educator: EducatorDep,
    course_id: ID,
) -> list[User]:
    try:
        return await enrollment_service.list_students(course_id, educator)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/student/enrollments", response_model=list[CourseRead])
async def list_student_courses(
    enrollment_service: CourseEnrollmentServiceDep,
    student: StudentDep,
) -> list[Course]:
    try:
        return await enrollment_service.list_student_courses(student)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/{course_id}/access", response_model=CourseRead)
async def assert_course_access(
    enrollment_service: CourseEnrollmentServiceDep,
    student: StudentDep,
    course_id: ID,
) -> Course:
    try:
        return await enrollment_service.assert_course_access(course_id, student)
    except CourseServiceException as e:
        raise course_http_exception(e) from e


@router.get("/me/chat-context", response_model=list[CourseChatContext])
async def get_chat_context(
    enroll: CourseEnrollmentServiceDep,
    user: CurrentUserDep,
) -> list[CourseChatContext]:
    try:
        courses = await enroll.list_accessible_courses(user)
        return [
            CourseChatContext(course=course, vectorstore=course.vectorstore)
            for course in courses
            if (course.vectorstore and course.vectorstore.status == "ready")
        ]
    except CourseServiceException as e:
        raise course_http_exception(e) from e
