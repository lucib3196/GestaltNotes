import asyncio
from pathlib import Path

from src.core.database_config import Session, engine
from src.core.settings import get_settings
from src.service.user.user_manager import UserCreate
from src.web.dependencies import SessionDep, get_user_manager

settings = get_settings()
print(settings.MODE)

user_manager = get_user_manager(SessionDep)
data = Path(r"src\batch\batch_emails.txt").read_text()
with Session(engine, expire_on_commit=False) as session:
    user_manager = get_user_manager(session)

    for d in data.split():
        create_data = UserCreate(password=d, email=d)
        asyncio.run(user_manager.create_user(create_data))
