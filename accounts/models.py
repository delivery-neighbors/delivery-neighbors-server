import os.path

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils import timezone


def avatar_upload_to(instance, filename):
    time_path = timezone.now().strftime('%Y_%m_%d_%T')
    filename_split = os.path.splitext(filename)
    img = filename_split[0]
    extension = filename_split[1].lower()

    return 'media/avatar/'+img + '_' + time_path + extension


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=20,
        null=False
    )
    avatar = models.ImageField(storage=S3Boto3Storage,
                               upload_to=avatar_upload_to,
                               default='media/avatar/default_img.jpg')
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # fcm token field -> user - fcm
    fcm_token = models.CharField(blank=True, max_length=500, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "user"

