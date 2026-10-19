import os
import random
import time
from dotenv import load_dotenv
from celery import Celery

from backend.core import get_settings

settings = get_settings()
load_dotenv()


app = Celery(
    "random_number",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL"),
)


@app.task()
def random_number(max_value):
    time.sleep(60)
    print("Processing......")
    return random.randint(0, max_value)
