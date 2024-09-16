
### Django install..
```bash
pip install django
```

### Django Extensions Package to clear pyc and cache
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
### Django Project Create..
```bash
django-admin startproject "projectname" .
django-admin startproject core .
```
### Django App Creating..
```bash
python manage.py startapp "appname"
```
### Server Running..
```bash
python manage.py runserver / python manage.py runserver 0.0.0.0:8000 --noreload
```

### Server Stop
```bash
Ctrl + C
```

### For database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### Clean Migrations
File : .env
```
APPS=app automation
```
Then run clean.py exist in Additional Features Folder
### To Update database if fail to upgrade need to follow these
```
delete db migrations or db
then delete all files from the migration folder of the app folder without __init__.py
```
### For Admin user creation
```bash
python manage.py createsuperuser
winpty python manage.py createsuperuser 
```

### Important folders..
```
templates
static
🔽 media
   ▶️ images 
```
### Change in static folder need to run this command / especially when application in server
```bash
python manage.py collectstatic
```
### Either image shows from static folder or database
```html
<img src="{% if request.user.profile_image %}{{request.user.profile_image.url}}{% else %}{% static "images/profile/user.png" %}{% endif %}" alt="" width="35" height="35" class="rounded-circle">
```

### 404 Page
```
404.html and Debug is false for 404 page
```

### CSS JS support
```html
{% load static %}
<link rel="stylesheet" href="{% static 'style.css' %}">
<script src="{% static 'myfirst.js' %}"></script>
```

### Changing the Django Admin Credit (admin.py)
```py
#  admin.py in Registered last App in setting will get top priority
from django.contrib import admin
admin.site.site_title = "My Custom Admin Title"
admin.site.site_header = "My Custom Admin Portal"
admin.site.index_title = "Welcome to Admin Dashboard"
```
### Changing the Django Admin Url (urls.py in project folder)
```py
from django.contrib import admin
urlpatterns = [
    path('custom-admin/', admin.site.urls),
] 
```

## Django Architecture
```
.env
▶️ core
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
