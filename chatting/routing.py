from django.urls import path

from . import consumers

urlpatterns = [
    path('ws/chatting/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
