from dotenv import load_dotenv
import os 
import time
import random


load_dotenv()

from celery import Celery
app = Celery(
    "random_number",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL")
    
)


@app.task()
def random_number(max_value):
    time.sleep(60)
    print("Processing......")
    return random.randint(0, max_value)