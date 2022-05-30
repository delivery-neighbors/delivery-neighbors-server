from django.urls import path
from chat import views

app_name = 'chat'
urlpatterns = [
    # 채팅방 생성 & 목록 조회
    path('room/', views.RoomGetCreateAPIView.as_view(), name='room-main'),
    # 단일 채팅방 조회 & 삭제
    path('room/<int:pk>', views.RoomRetrieveDestroyAPIView.as_view(), name='room-sub'),
    # 카테고리 조회
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    # 유저 채팅방 참여
    path('room/<int:room_id>/users/', views.ChatUserView.as_view(), name='chat_user'),
]
