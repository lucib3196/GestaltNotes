from pydantic import BaseModel

from .notes.schema import CourseNoteDelete as CourseNoteDelete
from .notes.schema import CourseNoteRead as CourseNoteRead
from .notes.schema import CourseNoteUpdate as CourseNoteUpdate


class CourseDelete(BaseModel):
    success: bool
    info: str
