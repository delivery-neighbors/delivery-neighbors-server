from django.db import models

from chat.models import ChatUser


class Pay(models.Model):
    chat_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    payment_key = models.CharField(max_length=20)
    order_id = models.DateTimeField(auto_now_add=True)
    amount = models.DateTimeField(auto_now=True)
