from django.urls import path
from chat import views

app_name = 'chat'
urlpatterns = [
    path('room/', views.RoomCreateAPIView.as_view(), name='room_create'),
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    # path('category/create', views.CategoryCreateView.as_view(), name='category-create'),
]
