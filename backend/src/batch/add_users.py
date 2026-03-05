from src.core.settings import get_settings
from src.web.dependencies import get_user_manager, SessionDep
from src.service.user.user_manager import UserCreate
from src.core.database_config import engine, Session
from pathlib import Path
import asyncio

settings = get_settings()
print(settings.MODE)

user_manager = get_user_manager(SessionDep)
data = Path(r"src\batch\batch_emails.txt").read_text()
with Session(engine, expire_on_commit=False) as session:
    user_manager = get_user_manager(session)

    for d in data.split():
        create_data = UserCreate(password=d, email=d)
        asyncio.run(user_manager.create_user(create_data))
