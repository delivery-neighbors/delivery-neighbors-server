import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'config': {
            # "hosts": [('127.0.0.1', 6379)],
            "hosts": [('redis', 6379)],
        }
    }
}

# ASGI application
ASGI_APPLICATION = 'config.asgi.local.application'
# WSGI application
WSGI_APPLICATION = 'config.wsgi.local.application'


