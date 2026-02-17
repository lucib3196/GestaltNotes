from .dependencies import CourseDBDependency
from src.model.course import Course, CourseData
from fastapi.routing import APIRouter
from uuid import UUID

router = APIRouter(prefix="/course", tags=["course"])


@router.post("/")
async def create_course(cdb: CourseDBDependency, data: CourseData) -> Course:
    return await cdb.create_course(data)


@router.get("/{id}")
async def get_course(cdb: CourseDBDependency, id: str | UUID):
    return await cdb.get_course(id)
