from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'
urlpatterns = [
    # kakao
    path('kakao/login/', views.kakao_login, name="kakao_login"),
    path('kakao/callback/', views.kakao_callback, name="kakao_callback"),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name="kakao_login_finish"),
    path('kakao/logout/', views.kakao_logout, name="kakao_logout"),

    # JWT login, signup
    path('deliveryneighbors/emailsend/', views.EmailSendView.as_view(), name='email-send'),
    path('deliveryneighbors/emailverify/', views.EmailVerifyView.as_view(), name='email-verify'),
    path('deliveryneighbors/signup/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('deliveryneighbors/signin/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('deliveryneighbors/signout/', views.UserLogoutAPIView.as_view(), name='user-logout'),
    path('deliveryneighbors/resign/', views.UserResignAPIView.as_view(), name='user-resign'),

    path('deliveryneighbors/reset_pwd/', views.PwdResetAPIView.as_view(), name='pwd-reset'),

    path('deliveryneighbors/token/refresh/', TokenRefreshView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
