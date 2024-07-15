# app_folder/tasks.py

# Must be write code organize way
# Must be seperate functions, instead of using inner function

from celery import shared_task

@shared_task
def content_creation_job(arg1, arg2):
    # Task logic goes here
    pass

# example 2

import logging
logger = logging.getLogger(__name__)
@shared_task(bind=True)
def celery_demo_task(self):
    for i in range(10):
        sleep(1)
        logger.info(i)
    return 'Done'


# After setup or update -> navigate to your Django project directory, and run the Celery worker
>>> celery -A project_name worker -l INFO   # replace with your project name


