from django.urls import path
from chatting import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:room_id>/<int:user_id>/', views.room, name='room'),
    path('room/<int:pk>/message/', views.MessageGetAPIView.as_view(), name='chat-message'),
]
