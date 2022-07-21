from django.urls import path

from payment import views

urlpatterns = [
    # 결제 승인
    path('toss/confirm/<int:chatuser>/', views.payConfirmed, name='pay_confirmed'),

    # 결제 정보 등록, 조회
    path('toss/info/<int:chatuser>/', views.PayCreateListAPIView.as_view(), name='pay-info'),
]
