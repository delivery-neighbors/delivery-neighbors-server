from django.db import models


class User(models.Model):
    nickname = models.CharField('NICKNAME', max_length=20)
    email = models.CharField('EMAIL', max_length=50)
    pwd = models.CharField('PWD', max_length=30)
    profile_img = models.ImageField('PROFILE_IMG')
    created_at = models.DateTimeField('CREATE DATE', auto_now_add=True)
