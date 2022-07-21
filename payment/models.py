from django.db import models

from chat.models import ChatUser


class Pay(models.Model):
    order_id = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
