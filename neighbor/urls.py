from django.urls import path

from neighbor import views

urlpatterns = [
    path('user/<int:pk>/', views.UserRetrieveAPIView.as_view()),

    # review
    path('review/', views.ReviewListAPIView.as_view()),
    path('review/<int:pk>/', views.ReviewRetrieveAPIView.as_view()),
    # path('user/<int:pk>/review/', views.UserReviewListAPIView.as_view()),
    # path('user/<int:pk>/review/', views.UserReviewCreateAPIView.as_view()),
]
