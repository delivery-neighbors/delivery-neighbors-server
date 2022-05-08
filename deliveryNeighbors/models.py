from django.db import models


class User(models.Model):
    nickname = models.CharField('NICKNAME', max_length=20)
    email = models.CharField('EMAIL', max_length=50)
    pwd = models.TextField('PWD')
    profile_img = models.ImageField('PROFILE_IMG', upload_to='images', null=True, blank=True)
    created_at = models.DateTimeField('CREATE DATE', auto_now_add=True)

    def __str__(self):
        return self.nickname
