#### Creating Environment
```bash
python -m venv env
```

#### Active envirment
```bash
Source scripts/env/activate
Source scripts/bin/activate   --linux/mac
```
#### VS Code terminal from Windows
```
Set-ExecutionPolicy RemoteSigned -Scope Process
.\env\Scripts\Activate
```
#### if need deactivate
```bash
deactivate
```


## Commands---------------------------------------
#### Django install..
```bash
pip install django
```

#### Install Django Extensions Package It will help to clear pyc and cache (Optional)
```bash
pip install django-extensions
```
```py
settings.py File
INSTALLED_APPS = (
  ...
  'django_extensions',
  ...
)
```
#### Django Project Create..
```bash
django-admin startproject "projectname" .
```
#### Django App Creating..
```bash
python manage.py startapp "appname"
```
#### Server Running..
```bash
python manage.py runserver / python manage.py runserver 0.0.0.0:8000 --noreload
```

#### Server Stop
```bash
Ctrl + C
```


#### To Update database if fail to upgrade need to follow these
```
delete db migrations or db
then delete all files from the migration folder of the app folder without __init__.py
```
#### For database update and first time need to run this command
```bash
python manage.py makemigrations
python manage.py migrate
```
#### For Admin
```bash
python manage.py createsuperuser
winpty python manage.py createsuperuser 
```

#### Important folders..
```
templates
static
🔽 media
   ▶️ images 
```
#### For static update, especially need when application in server
#### After any File update of static folder, CSS, JS, Images need to run this command
```bash
python manage.py collectstatic
```
#### We can use this command either image shows from static folder or database
```html
<img src="{% if request.user.profile_image %}{{request.user.profile_image.url}}{% else %}{% static "images/profile/user.png" %}{% endif %}" alt="" width="35" height="35" class="rounded-circle">
```

#### 404 Page
```
404.html and Debug is false for 404 page
```

#### CSS JS support
```html
{% load static %}
<link rel="stylesheet" href="{% static 'style.css' %}">
<script src="{% static 'myfirst.js' %}"></script>
```

#### Changing the Django Admin Header Text
#### admin.py in any App, Registered last App in setting will get top priority
```py
admin.site.site_header = 'Project Name'   
```

## Django Architecture
```
.env
▶️ project
▶️ app1
▶️ app2
🔽 static
   ▶️ css
   ▶️ js
   ▶️ images
🔽 templates
   📄 base.html
   ▶️ app1
      📄 file.html
   ▶️ app2
      📄 file.html
🔽 media
   ▶️ images 
manage.py
```
