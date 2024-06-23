#!/bin/bash

# Ensure the script exits on error
set -e

if [ -z "$1" ]; then
    echo "No project name was supplied!"
    echo -e ">\t ./setup.sh <project_name>"
    exit 1
fi

# Variables (customize these as needed)
PROJECT_NAME=$1
DJANGO_SUPERUSER_USERNAME="admin"
DJANGO_SUPERUSER_PASSWORD="adminpassword"
DJANGO_SUPERUSER_EMAIL="admin@example.com"
POSTGRES_USER=user
POSTGRES_PASSWORD=password

# Create virtual environment
echo "Creating virtual environment..."
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    python3 -m venv venv
    source venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    python -m venv venv
    source venv/Scripts/activate
else
    echo "Unsupported OS type: $OSTYPE"
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
pip install django psycopg2-binary gunicorn

# Create Django project
echo "Creating Django project..."
django-admin startproject $PROJECT_NAME

# Change to project directory
cd $PROJECT_NAME

# Create .env file
cat <<EOF > .env
# Common settings
DJANGO_SECRET_KEY=$(openssl rand -base64 32)
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL settings
POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$PROJECT_NAME

# Django superuser settings for automated creation
DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL

# Project-specific settings
PROJECT_NAME=$PROJECT_NAME
EOF


# Create production Dockerfile
echo "Creating Dockerfile..."
cat << EOF > Dockerfile
FROM python:3.9

# Install necessary packages
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev libpq-dev cron && \
    apt-get clean

# Copy the cron job file into the container
COPY docker_prune.sh /docker_prune.sh

# Make the script executable
RUN chmod +x /docker_prune.sh

# Add cron job to crontab
# Run everyday 2 am
RUN echo "0 2 * * * /docker_prune.sh >> /var/log/docker_prune.log 2>&1" > /etc/cron.d/docker-prune

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/docker-prune

# Apply cron job
RUN crontab /etc/cron.d/docker-prune

# Create application directory
WORKDIR /opt/app

# Copy application code
COPY requirements.txt /opt/app/
RUN pip install -r requirements.txt
COPY . /opt/app/

# Set execute permission for entrypoint script
RUN chmod +x /opt/app/entrypoint.sh

# Define entrypoint
# Start cron daemon and the entrypoint script
CMD ["sh", "-c", "cron && /opt/app/entrypoint.sh"]
EOF

# Create production Dockerfile
echo "Creating docker_prune.sh..."
cat << EOF > docker_prune.sh
#!/bin/sh
docker system prune -a -f
EOF


# Create docker-compose file
echo "Creating docker-compose.yml..."
cat << EOF > docker-compose.yml
version: '3'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: $PROJECT_NAME
      POSTGRES_USER: $POSTGRES_USER
      POSTGRES_PASSWORD: $POSTGRES_PASSWORD
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
      - myproject-network

  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: /opt/app/entrypoint.sh
    volumes:
      - .:/opt/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - myproject-network

  nginx:
    image: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./nginx/certs:/etc/letsencrypt
      - ./nginx/www:/var/www/certbot
    depends_on:
      - web
    networks:
      - myproject-network

  certbot:
    image: certbot/certbot
    volumes:
      - ./nginx/certs:/etc/letsencrypt
      - ./nginx/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
    networks:
      - myproject-network

volumes:
  postgres_data:

networks:
  myproject-network:
EOF

# Create demo docker compose with celery
cat << EOF > docker_compose_with_celery.md
version: '3'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: $PROJECT_NAME
      POSTGRES_USER: $POSTGRES_USER
      POSTGRES_PASSWORD: $POSTGRES_PASSWORD
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
      - myproject-network

  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: /opt/app/entrypoint.sh
    volumes:
      - .:/opt/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
      - celery_worker1
      - celery_worker2
    networks:
      - myproject-network

  nginx:
    image: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./nginx/certs:/etc/letsencrypt
      - ./nginx/www:/var/www/certbot
    depends_on:
      - web
    networks:
      - myproject-network

  certbot:
    image: certbot/certbot
    volumes:
      - ./nginx/certs:/etc/letsencrypt
      - ./nginx/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
    networks:
      - myproject-network

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    networks:
      - myproject-network

  celery_worker_app1:
    build: .
    command: celery -A $PROJECT_NAME worker -Q app1 -l info
    # command: celery -A $PROJECT_NAME worker -Q app1 -1 info --concurrency=10
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$PROJECT_NAME
      - REDIS_URL=redis://redis:6379

  celery_worker_app2:
    build: .
    command: celery -A $PROJECT_NAME worker -Q app2 --loglevel=info
    # command: celery -A $PROJECT_NAME worker -Q app2 --loglevel=info --concurrency=10
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$PROJECT_NAME
      - REDIS_URL=redis://redis:6379

  volumes:
    postgres_data:

  networks:
    myproject-network:
EOF

# Create requirements.txt
echo "Creating requirements.txt..."
cat << EOF > requirements.txt
Django>=3.0,<4.0
psycopg2-binary
gunicorn
EOF


# Create GitHub Actions workflow for CI/CD
echo "Creating GitHub Actions workflow..."
mkdir -p .github/workflows
cat << EOF > .github/workflows/ci.yml
name: Django CI/CD

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_DB: $PROJECT_NAME
          POSTGRES_USER: $POSTGRES_USER
          POSTGRES_PASSWORD: $POSTGRES_PASSWORD
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:latest
        ports:
          - 6379:6379

    env:
      DATABASE_URL: postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$PROJECT_NAME
      REDIS_URL: redis://localhost:6379

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python manage.py test

  deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Log in to DockerHub
      uses: docker/login-action@v1
      with:
        username: \${{ secrets.DOCKER_USERNAME }}
        password: \${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: \${{ secrets.DOCKER_USERNAME }}/$PROJECT_NAME:latest

    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.3
      with:
        host: \${{ secrets.SERVER_HOST }}
        username: \${{ secrets.SERVER_USER }}
        key: \${{ secrets.SERVER_SSH_KEY }}
        script: |
          docker pull \${{ secrets.DOCKER_USERNAME }}/$PROJECT_NAME:latest
          docker-compose down --rmi all
          docker-compose up --build -d
          docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d \${{secrets.DOMAIN_NAME}} -d www.\${{secrets.DOMAIN_NAME}}

    - name: Update Nginx configuration
      run: |
        chmod +x ./update_nginx.sh
        ./update_nginx.sh \${{ secrets.DOMAIN_NAME }} \${{secrets.SERVER_HOST}}
EOF


# Create entrypoint.sh
cat <<EOF > entrypoint.sh
#!/bin/sh

# Exit on error
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << EOS
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created.')
else:
    print(f'Superuser {username} already exists.')
EOS

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn ${PROJECT_NAME}.wsgi:application --bind 0.0.0.0:8000
EOF

chmod +x entrypoint.sh

# Create nginx directory and config
mkdir nginx
cat <<'EOF' > nginx/nginx.conf
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location /static/ {
        alias /home/app/web/staticfiles/;
        expires 30d;
        access_log off;
    }

    location /media/ {
        alias /opt/app/media/;
        expires 30d;
        access_log off;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}

server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate /etc/letsencrypt/live/localhost/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/localhost/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/app/web/staticfiles/;
        expires 30d;
        access_log off;
    }

    location /media/ {
        alias /opt/app/media/;
        expires 30d;
        access_log off;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}
EOF

# Updating Nginx SH for Production Server
cat <<'EOF' > update_nginx.sh
#!/bin/sh

# Your domain name (this will be provided by the CI/CD environment)
DOMAIN=$1
IP_ADDRESS=$2

# Path to your nginx configuration file
NGINX_CONFIG="nginx/nginx.conf"

# Replace "localhost" with your domain name in nginx.conf
sed -i "s/server_name localhost;/server_name $DOMAIN;/g" $NGINX_CONFIG
# Replace "localhost" from .env
sed -i "s/DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1;/DJANGO_ALLOWED_HOSTS=$DOMAIN,$IP_ADDRESS;/g" ".env"
EOF




mkdir -p static media templates staticfiles logs
touch logs/console.log

# Update Django settings for database and static/media files
# Modify settings.py to read from .env file
cat <<EOF >> ${PROJECT_NAME}/settings.py

import os
from dotenv import load_dotenv
from pathlib import Path
from django.conf import settings
import logging
load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')

# Also, need to Configure urls.py file for media support 
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles" # for collect static


DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("SQL_HOST", "localhost"),
        'PORT': os.environ.get("SQL_PORT", "5432"),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(Path(settings.BASE_DIR) / 'logs' / 'console.log'),
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}


# in views.py or any other files
logger = logging.getLogger("django")
logger.info('Message')
EOF

# Readme File
cat <<'EOF' > readme.md
## Project Structure
```
▶️ venv
🔽 .github/workflows
  📄 ci.yml
▶️ project_dir
📄 Dockerfile
📄 docker-compose.yml
📄 requirements.txt
📄 .env
📄 entrypoint.sh
📄 docker_prune.sh
📄 update_nginx.sh
📄 manage.py
📄 readme.md
```

# Docker Compose Usage
```bash
docker-compose up                                            // Build from scratch
docker-compose up --build                                    // build and rebuild with existing
docker-compose exec web python manage.py makemigrations
// calling docker(docker-compose) -> execute(exec) -> defined image name (web) -> python command (python manage.py makemigrations)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser admin admin admin@admin.com
docker-compose down                                // Down will remove container and images
docker-compose down -v                             // -v flag removes named volumes declared 
docker-compose stop                                // simply stop docker without remove anything
docker system prune -a -f                          // Remove All Containers

docker-compose logs -f                // View Logs
docker-compose exec web sh            // Interactive Shell:


docker-compose logs -f celery_worker   // Verify Celery Worker
docker stats                           // CPU Memory Network Block status
docker stats your_container_name
docker logs your_container_name
docker-compose logs celery_worker_app1   // celery worker1 logs
docker-compose logs celery_worker_app2   // celery worker2 logs
```

## How to add Docker secrect key in github action
```
https://github.com/samratpro/{repo_name}/settings/secrets/actions/new

Name * : (Input Field) DOCKER_USERNAME
Secret * : your_docker_username
Click on Add Secrect Button

Name * : (Input Field) DOCKER_PASSWORD
Secret * : your_docker_password
Click on Add Secrect Button

Name * : (Input Field) SERVER_HOST
Secret * : cloud_ip_address
Click on Add Secrect Button

Name * : (Input Field) SERVER_USER
Secret * : cloud_ip_username
Click on Add Secrect Button

Name * : (Input Field) SERVER_SSH_KEY
Secret * : ssh_key_from_cloud
Click on Add Secrect Button

Name * : (Input Field) DOMAIN_NAME
Secret * : example.com
Click on Add Secrect Button
```

## Generate SSH Keys To Connect between Server and Github
```
  >>> ssh-keygen -t ed25519 -C "your_email@example.com"   
  >>> Enter file in which to save the key (path): _empty_ ENTER
  >>> Enter passphrase (empty for no passphrase): _empty_ ENTER
  >>> Enter same passphrase again: _empty_ ENTER

- If Permission Denied then Own .ssh then try again to Generate SSH Keys after this:
  >>> sudo chown -R user_name(example:root) .ssh
                  
- Key will generate, copy that
- To see the key again after clear
            >>> cat ~/.ssh/id_ed25519.pub
 - Will Open Public SSH Keys then copy the key
```
## Prepare Server
```sh
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
```
## Deploy to Server - Push code to GitHub
```sh
git add .
git commit -m "Setup local Docker and CI/CD"
git push origin main
```
```
GitHub Actions will automatically build, test, and deploy
```
# Cerbot for SSL in server
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d your_domain -d www.your_domain
EOF

echo "Setup complete. You can now start developing your Django project."
