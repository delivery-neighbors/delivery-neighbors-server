from firebase_admin import messaging
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from config.authentication import CustomJWTAuthentication

from accounts.models import User
from chat.models import Room, ChatUser

from rest_framework import status
from rest_framework.response import Response


def push_recommend_notification(self, request):
    user_id = CustomJWTAuthentication.authenticate(self, request)
    fcm_token = User.objects.get(id=user_id).fcm_token

    message = messaging.Message(
        notification=messaging.AndroidNotification(
            title='추천 이웃 채팅방 개설',
            body='추천 이웃이 개설한 채팅방 보기',
            click_action='대기화면 액티비티 이름 넣기'  #TODO
        ),
        token=fcm_token,
    )

    try:
        response = messaging.send(message)
        print(response)
    except Exception:
        print("fcm 전송 예외 발생", Exception)


@api_view(('GET',))
def push_chat_notification(request, room_id):
    room = Room.objects.get(id=room_id)
    chat_users = list(ChatUser.objects.filter(room=room))
    print("chat_users", chat_users)
    users = [chat_user.user for chat_user in chat_users]
    print("users", users)
    user_tokens = [user.fcm_token for user in users]
    print("user_tokens", user_tokens)
    return user_tokens
