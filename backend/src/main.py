import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter

from src.core.logger import logger
from src.core.database_config import create_db_and_tables
from src.core.firebase import initialize_firebase_app
from src.core.settings import get_settings
from src.web import ALL_ROUTES
from src.data.role import RoleDB
from src.core.database_config import SessionDep, Session


settings = get_settings()


## Intializes the database
@asynccontextmanager
async def on_startup(app: FastAPI):
    engine = create_db_and_tables()
    initialize_firebase_app()
    logger.info("Created database successfully")

    logger.debug("Seeding roles")
    with Session(engine) as session:
        await RoleDB(session).seed_roles()
        logger.info("[Initialization] Roles Created/verified Successfully")
        session.commit()

    yield


def add_routes(app: FastAPI, routes: list[APIRouter] = ALL_ROUTES):
    for r in routes:
        app.include_router(r)


def get_app():
    app = FastAPI(title=settings.PROJECT_NAME, lifespan=on_startup)
    logger.info("[Initialization] Initialized app")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS
        ],  # allow specific frontend origins
        allow_credentials=True,  # allow cookies, Authorization headers
        allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],  # allow all headers (including Authorization)
        expose_headers=["Content-Disposition"],
    )

    add_routes(app)
    return app


app = get_app()


def main():
    uvicorn.run(
        "src.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8010)),
        reload=True,
    )


if __name__ == "__main__":
    main()
