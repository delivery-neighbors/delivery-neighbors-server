from django.urls import path

from chatting import consumers

websocket_urlpatterns = [
    path('ws/chatting/<str:room_name>/<int:user_id>/', consumers.ChatConsumer.as_asgi()),
]
