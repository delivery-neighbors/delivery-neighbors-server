from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['https://baedalius.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'baedaliusdb',
        'USER': 'admin',
        'PASSWORD': 'mariadb12',
        'HOST': 'baedaliusdb.cbuqzssoipo8.ap-northeast-2.rds.amazonaws.com',
        'PORT': 3306,
    }
}

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'config': {
            "hosts": [('baedalius.com', 6379)],
        }
    }
}

# ASGI application
ASGI_APPLICATION = 'config.asgi.prod.application'
# WSGI application
WSGI_APPLICATION = 'config.wsgi.prod.application'
