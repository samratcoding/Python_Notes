```bash
pip install django-ckeditor
```
## setting.py
```py
INSTALLED_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    ]
```
## setting.py
```py
# CKEditor Settings >>>>>>>>>>>>>>>>
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' 

CKEDITOR_CONFIGS = {
    'default':
        {
            'toolbar': 'full',
            'width': 'auto',
            'extraPlugins': ','.join([
                'codesnippet',
            ]),
        },
}
```

## models.py
```py
from ckeditor_uploader.fields import RichTextUploadingField
class MyModel(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True, null=True)
    def __str__(self):
        return self.name
```
## project > urls.py
```py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
## command
```bash
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
```
# CK-Editor in HTML
```html
{% extends 'dashboard.html' %}
{% block dashboardcontent %}
{% load static %}
<script src="{% static 'ckeditor/ckeditor-init.js' %}"></script>
<script src="{% static 'ckeditor/ckeditor/ckeditor.js' %}"></script>

<div class="container mt-5">
    <h1> {{post.name}} </h1>
    <textarea name="content" id="id_content">{{ post.content }}</textarea>
    <script>
        CKEDITOR.replace('id_content');
    </script>
</div>

{% endblock dashboardcontent %}
```
## Also we can get data from HTML CK-Editor and save in Database, views.py
```py
def save_content(request):
    if request.method == 'POST':
        content = request.POST.get('content')
    else:
        pass
```

