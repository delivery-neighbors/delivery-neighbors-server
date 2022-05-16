from django.urls import path
from deliveryNeighbors import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'deliveryNeighbors'
urlpatterns = [
                  path('deliveryneighbors/emailsend/', views.EmailSendView.as_view(), name='email-send'),
                  path('deliveryneighbors/emailverify/', views.EmailVerifyView.as_view(), name='email-verify'),
                  path('deliveryneighbors/signup/', views.UserCreateAPIView.as_view(), name='user-create'),
                  # path('deliveryneighbors/signin/', views.UserLoginAPIView.as_view(), name='user-login'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
