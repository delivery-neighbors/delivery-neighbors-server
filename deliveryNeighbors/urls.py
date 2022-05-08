from django.urls import path
from deliveryNeighbors import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'deliveryNeighbors'
urlpatterns = [
    path('deliveryneighbors/signup/', views.UserCreateAPIView.as_view(), name='user-create')
    # path('deliveryneighbors/signin/'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
