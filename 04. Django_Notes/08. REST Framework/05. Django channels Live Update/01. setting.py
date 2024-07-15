# pip install channels
# pip install channels_api

# Install app in setting

INSTALLED_APPS = [
    '.......',
    'channels',
]


# Add channels middleware
MIDDLEWARE = [
    # ...
    'channels.middleware.WebSocketMiddleware',
]

# Configure channels-allowed-hosts
CHANNELS_API = {
    "ALLOWED_HOSTS": ["*"],
}
