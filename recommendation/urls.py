from django.urls import path

from recommendation import views

urlpatterns = [
    path('user/<int:pk>/similaruser/', views.SimilarUserListView.as_view()),
]
