from django.urls import path

from payment import views

urlpatterns = [
    # openbank
    path('openbank/authorize/', views.openbank_authorize, name="openbank_authorize"),
    path('openbank/callback/', views.openbank_callback, name="openbank_callback"),
    # path('openbank/token/', views.openbank_token, name="openbank_token"),
    # path('openbank/authorize_account/', views.authorize_account, name="authorize_account"),
    # path('openbank/deposit/', views.deposit)  # 입금 api
]