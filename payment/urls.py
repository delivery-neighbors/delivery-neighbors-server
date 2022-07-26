from django.urls import path

from payment import views

urlpatterns = [

    # 결제 정보 등록, 조회
    path('toss/info/<int:chatuser>/', views.PayCreateListAPIView.as_view(), name='pay-info'),

    # 결제 성공 및 결제 승인
    path('toss/confirm/', views.pay_confirmed, name='pay_confirmed'),

    # 결제 실패
    path('toss/fail/', views.pay_failed, name='pay_failed')
]
