from django.urls import path

from recommendation import views

urlpatterns = [
    path('user/similaruser/', views.SimilarUserListView.as_view()),
]
