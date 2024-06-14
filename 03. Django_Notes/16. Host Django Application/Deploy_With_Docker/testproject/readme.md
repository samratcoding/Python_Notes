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

# Docker Compose
```
docker-compose up --build
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser admin admin admin@admin.com
docker-compose down
docker-compose down -v # -v flag removes named volumes declared 

docker-compose logs -f                 # View Logs
docker-compose exec web sh             # Interactive Shell:
docker system prune -a -f              # Remove All Containers

docker-compose logs -f celery_worker   # Verify Celery Worker
docker stats                           # CPU Memory Network Block status
docker stats your_container_name
docker logs your_container_name

docker-compose logs celery_worker_app1   # celery worker1 logs
docker-compose logs celery_worker_app2   # celery worker2 logs
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
