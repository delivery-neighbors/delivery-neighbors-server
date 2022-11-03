from django.contrib import admin

from chatting.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_user_id', 'room_id', 'message']


admin.site.register(Message, MessageAdmin)
