from django.contrib import admin
from django.urls import path
from deliveryNeighbors import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserCreateAPIView.as_view(), name='user-create'),
]
