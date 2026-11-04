from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import update
from sqlmodel import Session, select

from backend.courses.models import NOTE_BLOCK_CONTENT_MODELS, NoteBlock
from backend.adapters import Repository


class NoteBlockRepo(Repository[NoteBlock, NoteBlockUpdate]):
    def __init__(self, session: Session)->None:
        self._session = session
        
        
    def 