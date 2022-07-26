from django.db import models


class ChatMessage(models.Model):
    sender = models.ForeignKey('chat.ChatUser', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
