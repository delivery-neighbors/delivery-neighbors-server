from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('deliveryNeighbors.urls')),
    path('accounts/kakao/login/', views.kakao_login, name="kakao_login"),
    path('accounts/kakao/callback/', views.kakao_callback, name="kakao_callback"),
    path('accounts/kakao/login/finish/', views.KakaoLogin.as_view(), name="kakao_login_finish"),
    path('accounts/kakao/logout/', views.kakao_logout, name="kakao_logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
