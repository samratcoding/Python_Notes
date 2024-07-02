version: '3'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: PROJECT_NAME
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
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

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    networks:
      - myproject-network

  celery_worker_app1:
    build: .
    command: celery -A test2 worker -Q app1 -l info
    # command: celery -A test2 worker -Q app1 -1 info --concurrency=10
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/PROJECT_NAME
      - REDIS_URL=redis://redis:6379

  celery_worker_app2:
    build: .
    command: celery -A test2 worker -Q app2 --loglevel=info
    # command: celery -A test2 worker -Q app2 --loglevel=info --concurrency=10
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/PROJECT_NAME
      - REDIS_URL=redis://redis:6379

  nginx:
    image: nginx
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
