from .base import *

DEBUG = True

ALLOWED_HOSTS = ['http://3.38.38.248']

CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['http://3.38.38.248']

secret_file = os.path.join(BASE_DIR, 'secrets-prod.json')
secrets = Secrets(secret_file)

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
