from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from chat import views

app_name = 'chat'
urlpatterns = [
    # 채팅방 생성 & 목록 조회
    path('room/', views.RoomGetCreateAPIView.as_view(), name='room-main'),
    # 단일 채팅방 조회 & 삭제
    path('room/<int:pk>/', views.RoomRetrieveDestroyAPIView.as_view(), name='room-sub'),
    # 채팅방 키워드 검색
    path('room/search/', views.RoomGetByKeywordView.as_view(), name='room-search'),

    # 카테고리 조회
    # path('category/', views.CategoryListView.as_view(), name='category-list'),

    # 유저 채팅방 참여, 나가기, 채팅방 참여 인원 조회
    path('room/<int:room_id>/neighbor/', views.ChatUserView.as_view(), name='chat-user'),

    # 실시간 위치 정보 입력 & 특정 채팅방에 속한 모든 유저 위치 조회
    path('room/cur_location/', views.CurrentLocationView.as_view(), name='user-location'),

    # 참여중인 채팅방 조회
    path('room/joined/', views.ChatJoinedView.as_view(), name='chat-joined'),

    # 수령 완료한 채팅방 조회
    path('room/joined/done/', views.ChatDoneListView.as_view(), name='chat-done-list'),

    # 채팅방 거래 완료 ; 거래 상태 변경(status=DONE)
    path('room/<int:room_id>/done/', views.ChatDoneView.as_view(), name='chat-done'),

    # 채팅방 목록에서 지우기
    path('room/<int:room_id>/delete/', views.ChatListDeleteView.as_view(), name='chat-delete'),

    # 방, 채팅 유저 상태 값 조회
    path('room/<int:pk>/status/', views.RoomWithUserStatusListView.as_view(), name='chat-status'),

    # 방 초기 정보
    path('room/<int:pk>/myinfo/', views.MyInfoByRoomAPIView.as_view(), name='chat-my-info'),

    # 채팅 유저 주문 금액 조회
    path('room/<int:pk>/payinfo/', views.ChatUserPayInfoAPIView.as_view(), name='chat-pay-info')
]
