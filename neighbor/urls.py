from django.urls import path

from neighbor import views

urlpatterns = [
    # 유저 정보
    path('user/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user-retrieve-update'),

    # review
    path('review/', views.ReviewListAPIView.as_view()),
    path('review/<int:pk>/', views.ReviewRetrieveAPIView.as_view()),
    path('user/<int:userid>/review/', views.UserReviewListAPIView.as_view()),
    path('user/<int:userid>/review/<int:reviewid>/', views.user_review_update),

    # 사용자 주소 설정, 조회, 삭제
    path('user/address/', views.UserAddressView.as_view(), name='user-address'),
    path('user/address/<int:pk>/', views.UserAddressDestroyView.as_view(), name='user-address-delete'),

    # map
    path('kakaomap/', views.kakao_map, name='kakao_map'),

    # 최근 검색어 조회, 삭제
    path('user/search/', views.UserRecentSearchView.as_view()),
    path('user/search/<int:pk>/', views.UserSearchDestroyAPIView.as_view()),
]
