from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from config import views

schema_view = get_schema_view(
    openapi.Info(
        title="deliveryNeighbors API",
        default_version='v1',
        description="배달 이웃 API 문서",
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # Swagger
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

    # allauth
    path('account/', include('allauth.urls')),

    path('admin/', admin.site.urls),
    path('v1/', include('deliveryNeighbors.urls')),
    path('accounts/kakao/login/', views.kakao_login, name="kakao_login"),
    path('accounts/kakao/callback/', views.kakao_callback, name="kakao_callback"),
    path('accounts/kakao/login/finish/', views.KakaoLogin.as_view(), name="kakao_login_finish"),
    path('accounts/kakao/logout/', views.kakao_logout, name="kakao_logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
