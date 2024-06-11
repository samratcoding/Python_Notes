# task.py
from celery import shared_task

@shared_task
def my_periodic_task():
    # Your periodic task logic here
    print("Executing periodic task...")

# celery.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'my-periodic-task': {
        'task': 'path.to.your.task.my_periodic_task',
        'schedule': crontab(minute='*/15'),  # Execute every 15 minutes
    },
}
