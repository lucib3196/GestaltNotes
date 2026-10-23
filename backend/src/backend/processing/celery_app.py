import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app = Celery(
    "lecture_processing",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL"),
    include=["backend.processing.tasks"],
)
