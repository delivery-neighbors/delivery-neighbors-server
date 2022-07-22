from django.db import models

from chat.models import ChatUser


class Pay(models.Model):
    chat_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20)
    amount = models.IntegerField()
