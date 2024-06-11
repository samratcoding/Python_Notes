# pip install djangorestframework
# pip install djangorestframework-simplejwt




# Add 'rest_framework', and 'rest_framework_simplejwt' to INSTALLED_APPS
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
]




# Add JWT authentication settings
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Set token lifetime as needed
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
}
