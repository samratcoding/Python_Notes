## Need to run and check redis server before run celery
```bash
redis-server
```
```
 After setup or update -> navigate to your Django project directory, and run the Celery worker
# Must open a new separate terminal and use these command
# All tasks with celery will show in this tab ---
# >>> celery -A project_name worker -l info                                 # replace project name (-l info / --loglevel=info )
# >>> celery -A project_name worker -l info --concurrency=10 -n worker1@%h  # Running 10 task in worker1  @%h = hostname
# >>> celery -A project_name worker -l info --concurrency=10 -n worker2     # Running 10 task in worker2
```


# Debug
```
# >>> celery -A project_name worker -l debug --concurrency=10 -n worker1@%h
```
