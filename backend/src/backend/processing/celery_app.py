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
app.conf.update(
    control_queue_durable=False,
    control_queue_exclusive=True,
    event_queue_durable=False,
    event_queue_exclusive=True,
)