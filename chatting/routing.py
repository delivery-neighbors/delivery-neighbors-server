from django.urls import path

from chatting import consumers

urlpatterns = [
    path('ws/chatting/<str:room_id>/<int:chat_user_id>/', consumers.ChatConsumer.as_asgi()),
]
