from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, profile_img):
        if not email:
            raise ValueError('회원 가입을 위해 이메일을 입력해 주세요')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            profile_img=profile_img)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, profile_img):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            profile_img=profile_img
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(max_length=20, null=False, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    profile_img = models.ImageField(blank=True, upload_to='images/%Y/%m/%d/',
                                    default='images/default_img.jpg')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'profile_img']

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
