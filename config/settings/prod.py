from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['https://baedalius.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'deliveryNeighbors',
        'USER': 'dnuser',
        'PASSWORD': 'dnpass',
        'HOST': 'db',
        'PORT': 3306,
    }
}

# WSGI application
WSGI_APPLICATION = 'config.wsgi.prod.application'
