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

# Docker Compose Usages
```bash
docker-compose up                                         # Build from scratch
docker-compose up --build                                 # build and rebuild with existing
docker-compose up -d --build                              # Rebuild images without logs
# Best pratice -d --build for server, and sometime need to try 2-3 times

docker-compose exec web python manage.py makemigrations


#calling docker(docker-compose) -> execute(exec) -> defined image name (web) -> python command (python manage.py makemigrations)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser admin admin admin@admin.com
docker-compose down                                # Down will remove container and images
docker-compose down -v                             # -v flag removes named volumes declared 
docker-compose stop                                # simply stop docker without remove anything
docker system prune -a -f                          # Remove All Containers

docker-compose logs -f                # View Logs
docker-compose exec web sh            # Interactive Shell:


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
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"   

# >> Enter file in which to save the key (path): _empty_ ENTER

# >> Enter passphrase (empty for no passphrase): _empty_ ENTER

# >> Enter same passphrase again: _empty_ ENTER

# If Permission Denied then Own .ssh then try again to Generate SSH Keys after this:
sudo chown -R user_name(example:root) .ssh  
# Key will generate, copy that
# To see the key again after clear
cat ~/.ssh/id_ed25519.pub
#Will Open Public SSH Keys then copy the key
```
## Prepare Server
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo apt-get install git
sudo mkdir -p /srv/django_project
sudo chown your_user:your_user /srv/django_project
cd ~/srv/django_project
git clone "repolink"
chmod +x entrypoint.sh
sudo lsof -i :80   # Verify Port Availability
sudo service apache2/others stop # If apache2 or any server exist
```
## Push code from Local to GitHub
```bash
git add .
git commit -m "Setup local Docker and CI/CD"
git push origin main
```
```
GitHub Actions will automatically build, test, and deploy
```
## Note
```
If use dockerhub repo for deploy then, .env add in .dockerignore
If github repo is public then, .env add in .gitignore
```
## Name Server / DNS config
```
- Login to Domain Panel or Cloudflare
- Navigate to Manage DNS
- Add Following Records:
```
| Type  | Host/Name | Value                   |
|-------|-----------|-------------------------|
| A     | @         | Your Remote Server IP   |
| A     | www       | Your Remote Server IP   |
| AAAA  | @         | Your Remote Server IPv6 |
| AAAA  | www       | Your Remote Server IPv6 |

### Find IPv6/inet6
```
- Login server linux
- >>> Run the command: ` ifconfig `
- Find `inet6` that started with 2 or 3
- example : 2a10:c700:1:649a::1
```
### Check it from Linux Server
```bash
dig domain.com
nslookup domain.com
```

## Cerbot for SSL in server
```bash
cd /srv/django_project

docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot -d your_domain -d www.your_domain

docker-compose up --build
```
