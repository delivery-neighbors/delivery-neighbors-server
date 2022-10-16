from django.db import models


class Recommended(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    rec_user1 = models.IntegerField(blank=True)
    rec_user2 = models.IntegerField(blank=True)
    rec_user3 = models.IntegerField(blank=True)
