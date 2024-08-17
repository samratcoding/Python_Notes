## 01. Install Celery
```bash
pip install celery
pip install django-celery-results
pip install redis
```
```
# Documentation :  https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django
```
## 02. Install Redis (if not installed)
- Windows, Download : https://www.memurai.com/
- Macos, Download   : https://redis.io/docs/install/install-redis/install-redis-on-mac-os/
## For Ubuntu
```bash
sudo apt update
sudo apt install redis-server
sudo apt-get install redis-server
redis-server # command to check redis server is running
```
## 03. run the Celery worker
- After setup or update -> navigate to your Django project directory, and run the Celery worker
- Must open a new separate terminal and use these command
- All tasks with celery will show in this tab
- worker1, worker2 is related with project/settings.py
```bash
celery -A project_name worker -l info                                 # replace project name (-l info or --loglevel=info )
celery -A project_name worker -l info --concurrency=10 -Q worker1     # Running 10 task in worker1 
celery -A project_name worker -l info --concurrency=10 -Q worker2     # Running 10 task in worker2
```

## 04. Debug
```
celery -A project_name worker -l debug --concurrency=10 -Q worker_name
```
# 05. celery in VPS
## 5.1 Install supervisor
``bash
sudo apt install supervisor
``

## 5.2 Navigate to Supervisor Configuration Directory:
``
cd /etc/supervisor/conf.d/
``
## 5.3 Create a New Configuration File:
``
sudo nano celery.conf
``
## 5.4 Enter Supervisor Configuration:
```
[program:celery-worker1]
command=/www/wwwroot/project_path/venv_path_venv/bin/celery -A project_name worker -l info --concurrency=10 -Q worker1
directory=/www/wwwroot/AI_Writing_SaaS/
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true

[program:celery-worker2]
command=/www/wwwroot/project_path/venv_path_venv/bin/celery -A project_name worker -l info --concurrency=10 -Q worker2
directory=/www/wwwroot/AI_Writing_SaaS/
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
### 5.5 for schedule
```
[program:celery-worker3]
command=/www/wwwroot/PROJECT_PATH/venv_path/bin/celery -A beat -l info
directory=/www/wwwroot/AI_Writing_SaaS/
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
## 5.6 Save and Exit:
```
Press Ctrl + O >>> then press Enter to save the file.
Press Ctrl + X to exit nano.
Update Supervisor Configuration:
```
## 5.7 Linux command
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart celery-worker1
sudo supervisorctl restart celery-worker2
```
## 5.8 Check celery is working
```
sudo service supervisor status
sudo supervisorctl status
```
```
Active: active (running) ...(time)
```
## 5.9 Stop Celery
```
sudo supervisorctl
stop celery-worker
```
## 5.10 To start again
```
start celery-worker
```

