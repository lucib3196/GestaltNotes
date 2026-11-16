from sqlmodel import Session

from backend.adapters.repository import Repository
from backend.chat.model import Prompt, PromptUpdate


class PromptRepo(Repository[Prompt, PromptUpdate]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Prompt)
