from django.urls import path

from notification import push_notification

urlpatterns = [
    path('chat_push/<int:room_id>/', push_notification.push_chat_notification),
]
