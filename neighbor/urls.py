from django.urls import path

from neighbor import views

urlpatterns = [
    # review
    path('review/', views.ReviewListAPIView.as_view()),
    path('review/<int:pk>/', views.ReviewRetrieveAPIView.as_view()),
    # path('user/<int:pk>/review/', views.UserReviewListAPIView.as_view()),
    # path('user/<int:pk>/review/', views.UserReviewCreateAPIView.as_view()),
]
