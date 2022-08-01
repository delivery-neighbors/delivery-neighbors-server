from django.urls import path
from chatting import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/<int:user_id>/', views.room, name='room'),
]