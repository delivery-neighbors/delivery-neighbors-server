from django.urls import path

from chatting import consumers

urlpatterns = [
    path('ws/chatting/<int:room_id>/<int:user_id>/', consumers.ChatConsumer.as_asgi()),
]
