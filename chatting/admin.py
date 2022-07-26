from django.contrib import admin

from chatting.models import ChatMessage


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'message', 'created_at']


admin.site.register(ChatMessage, ChatMessageAdmin)
