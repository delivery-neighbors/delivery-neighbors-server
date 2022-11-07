import json
from datetime import timedelta
from pathlib import Path

import firebase_admin
from firebase_admin import credentials

import os

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Secrets:
    def __init__(self, secret_file):
        with open(secret_file) as f:
            self.secrets = json.loads(f.read())

    def get_secret(self, setting):
        try:
            return self.secrets.get(setting)
        except:
            error_msg = f'Set the {setting} environment variable'
            raise ImproperlyConfigured(error_msg)


# SECURITY WARNING: keep the secret key used in production secret!
secret_file = os.path.join(BASE_DIR, 'secrets.json')
secrets = Secrets(secret_file)

SECRET_KEY = secrets.get_secret("SECRET_KEY")
EMAIL_HOST_USER = secrets.get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = secrets.get_secret("EMAIL_HOST_PASSWORD")

private_key_id = secrets.get_secret("private_key_id")
private_key = secrets.get_secret("private_key")
client_email = secrets.get_secret("client_email")
client_id = secrets.get_secret("client_id")
auth_provider_x509_cert_url = secrets.get_secret("auth_provider_x509_cert_url")
client_x509_cert_url = secrets.get_secret("client_x509_cert_url")

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'

INSTALLED_APPS = [
    # app
    'accounts',
    'neighbor',
    'chat',
    'payment',
    'chatting',
    'recommendation',

    # channels
    'channels',

    # S3
    # 'storages',

    # jwt
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django-rest-framework
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    # dj-rest-auth
    "dj_rest_auth",
    "dj_rest_auth.registration",

    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',

    # api 문서 자동화
    'drf_yasg',

    # 스케줄러
    'django_apscheduler',

    # jupyter-notebook
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    # Serializer default permission class definition ; view permission class 정의 x 시 참조
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# # Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-allauth 유저 인증 로직
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# django 내장 메일 전송 기능
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.naver.com"
# TODO
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

REST_USE_JWT = True

JWT_SECRET_KEY = secrets.get_secret("JWT_SECRET_KEY")

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': JWT_SECRET_KEY,
}

SOCIAL_OAUTH_CONFIG = {
    'KAKAO_REST_API_KEY': secrets.get_secret('KAKAO_REST_API_KEY'),
    "KAKAO_REDIRECT_URI": secrets.get_secret('KAKAO_REDIRECT_URI'),
    "KAKAO_SECRET_KEY": secrets.get_secret('KAKAO_SECRET_KEY')
}

# django-jobs
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default
SCHEDULER_DEFAULT = True

# Toss Payments
TOSS_PAYMENTS_CONFIG = {
    'TOSS_API_KEY': secrets.get_secret('TOSS_API_KEY'),
    'TOSS_SECRET_KEY': secrets.get_secret('TOSS_SECRET_KEY')
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = secrets.get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = secrets.get_secret('AWS_SECRET_ACCESS_KEY')

AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'deliveryneighborsbucket'
AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)

AWS_QUERYSTRING_AUTH = False

# firebase admin sdk (for fcm)
service_account_json = {
  "type": "service_account",
  "project_id": "delivery-neighbors",
  "private_key_id": private_key_id,
  "private_key": private_key,
  "client_email": client_email,
  "client_id": client_id,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
  "client_x509_cert_url": client_x509_cert_url
}

cred = credentials.Certificate(service_account_json)
firebase_admin.initialize_app(cred)
