from django.urls import path
from chatting import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:room_id>/<int:chat_user_id>/', views.room, name='room'),
]
