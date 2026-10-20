from uuid import UUID

from celery import chain
from celery.result import AsyncResult
from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette import status

from backend.processing.celery_app import app
from backend.processing.schema import LectureTaskResponse, TaskProgress
from backend.processing.tasks import update_course_docs
from backend.web.courses.dependencies import CourseNoteServiceDep

ID = UUID | str

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/notes/{note_id}")
async def process_file(note_id: UUID, course_notes: CourseNoteServiceDep):
    note = await course_notes.get_note(note_id)
    if note.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="PDF Files are only supported type right now",
        )
    workflow = chain(
        app.signature(
            "backend.processing.tasks.get_raw_lecture_output", args=[str(note.file_id)]
        ),
        app.signature("backend.processing.tasks.vectorize_documents"),
    )
    task = workflow.apply_async()
    return {
        "file_id": note.file_id,
        "task_id": task.id,
        "summary": "Processing lecture",
    }


@router.get("/file/{task_id}", response_model=LectureTaskResponse)
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=app)
    return LectureTaskResponse(
        task_id=task_id,
        status=task.state,
        progress=(
            TaskProgress.model_validate(task.info) if task.state == "PROGRESS" else None
        ),
        result=task.result if task.successful() else None,
        error=str(task.result) if task.failed() else None,
    )


@router.post("/course/{course_id}/{note_id}/temp")
async def check(course_id: UUID, note_id: UUID):
    workflow = update_course_docs.s(course_id, note_id)
    task = workflow.apply_async()
    return {
        "course_id": course_id,
        "note_id": note_id,
        "task_id": task.id,
        "summary": "Processing lecture",
    }
