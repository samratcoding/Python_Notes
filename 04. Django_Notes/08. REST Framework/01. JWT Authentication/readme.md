## Install Module and Create App
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
python manage.py startapp api
```
## Config settings.py
```py
from datetime import timedelta

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]


# REST Framework configurations
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
CORS_ALLOW_ALL_ORIGINS = True
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```
## Config project's urls.py
```
urlpatterns = [
    path('api/', include('api.urls')),
]
```