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
        title="accounts API",
        default_version='v1',
        description="배달 이웃 API 문서",
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # allauth
    path('account/', include('allauth.urls')),

    # apps
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),

    # Swagger
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
