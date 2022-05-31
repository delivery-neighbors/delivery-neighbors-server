import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = []

secret_file = os.path.join(BASE_DIR, 'secrets.json')
secrets = Secrets(secret_file)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

