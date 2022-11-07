from django.db import models

from chat.models import ChatUser, Room


class Message(models.Model):
    chat_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
