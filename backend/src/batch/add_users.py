import asyncio
from pathlib import Path

from src.core.database_config import Session, engine
from src.core.settings import get_settings
from src.service.user.user_manager import UserCreate
from src.service.user.user_manager import UserManager
from sqlmodel import create_engine
settings = get_settings()
print(settings.ENV)
print(settings.DATABASE_URL)
engine = create_engine(
        url=settings.DATABASE_URL,
        echo=True,
        connect_args={},  # always a dict, never None
    )

data = Path(r"src/batch/batch_emails.txt").resolve().read_text()
with Session(engine, expire_on_commit=False) as session:
    user_manager = UserManager(session)

    for d in data.split():
        print(d)
        create_data = UserCreate(password=d, email=d)
        asyncio.run(
            user_manager.safe_create(
                create_data, role="student", force_password_reset=True
            )
        )
