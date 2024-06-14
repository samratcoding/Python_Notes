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

# SQLite settings for local development
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# PostgreSQL settings for production (commented out for reference)
# Uncomment and set these for production use
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=my_db
# DB_USER=my_user
# DB_PASSWORD=my_password
# DB_HOST=database
# DB_PORT=5432

# Django superuser settings for automated creation
DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL

# Project-specific settings
PROJECT_NAME=$PROJECT_NAME
EOF


# Create Local Dockerfile
cat <<EOF > Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Install dependencies
RUN apk add --no-cache build-base linux-headers postgresql-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /opt/app

# Copy the current directory contents into the container at /opt/app
COPY . /opt/app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint.sh executable
RUN chmod +x /opt/app/entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Run the Gunicorn server
CMD ["/opt/app/entrypoint.sh"]
EOF

# Create Local docker-compose file
echo "Creating docker-compose.yml..."
cat << EOF > docker-compose.yml
version: '3'

services:
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
    networks:
      - myproject-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web
    networks:
      - myproject-network

networks:
  myproject-network:
EOF



# Create production Dockerfile
echo "Creating Dockerfile.prod..."
cat << EOF > Dockerfile.prod
FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev libpq-dev && \
    apt-get clean

WORKDIR /opt/app

COPY requirements.txt /opt/app/
RUN pip install -r requirements.txt

COPY . /opt/app/

RUN chmod +x /opt/app/entrypoint.sh

ENTRYPOINT ["/opt/app/entrypoint.sh"]
EOF


# Create production docker-compose file
echo "Creating docker-compose.prod.yml..."
cat << EOF > docker-compose.prod.yml
version: '3'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
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

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: $PROJECT_NAME
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
      - myproject-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - .:/opt/app
    depends_on:
      - web
    networks:
      - myproject-network

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
python-dotenv
dj-database-url
EOF


# Create GitHub Actions workflow for CI/CD
echo "Creating GitHub Actions workflow..."
mkdir -p .github/workflows
cat << EOF > .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: \${{ secrets.DOCKER_USERNAME }}
          password: \${{ secrets.DOCKER_PASSWORD }}

      - name: Update Nginx configuration
        run: |
          chmod +x ./update_nginx.sh
          ./update_nginx.sh \${{ secrets.DOMAIN_NAME }}

      - name: Build and push Docker image
        run: |
          docker buildx build --platform linux/amd64,linux/arm64 -t your_image_name:latest -f Dockerfile.prod .
          docker push your_image_name:latest

      - name: Deploy with Docker Compose
        run: |
          docker-compose -f docker-compose.prod.yml up -d
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

if not User.objects.filter(username=username).exists():
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
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/app/static/;
        expires 30d;
        access_log off;
    }

    location /media/ {
        alias /opt/app/media/;
        expires 30d;
        access_log off;
    }

    # Optionally add security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";
}
EOF

# Updating Nginx SH for Production Server
cat <<'EOF' > update_nginx.sh
#!/bin/sh

# Your domain name (this will be provided by the CI/CD environment)
DOMAIN=$1

# Path to your nginx configuration file
NGINX_CONFIG="nginx/nginx.conf"

# Replace "localhost" with your domain name in nginx.conf
sed -i "s/server_name localhost;/server_name $DOMAIN;/g" $NGINX_CONFIG
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

# Also, need to Configure urls.py file for ` media support ` 
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
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
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



echo "Setup complete. You can now start developing your Django project."
