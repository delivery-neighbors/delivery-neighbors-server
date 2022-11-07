import json

from rest_framework import status
from rest_framework.response import Response

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from firebase_admin import messaging

from ai.cleanbot.cleanbot import return_bad_words_index
from accounts.models import User
from chat.models import Room, ChatUser
from chatting.serializers import ChattingUserSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    print("ChatConsumer")

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        # self.user_name = 'jiwoo'

    async def connect(self):
        print("[CONNECT]")

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        print(f"CONNECT >> kwargs: {self.scope['url_route']['kwargs']}")
        print(f"CONNECT >> rood_id: {self.room_id}")
        self.group_name = 'chat_room_%s' % self.room_id
        print(f"CONNECT >> group_name: {self.group_name}")

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )
        print(f"CONNECT >> channel_name: {self.channel_name}")
        print(f"CONNECT >> channel_layer: {self.channel_layer}")

        await self.accept()

    async def disconnect(self, close_cod):
        print("[DISCONNECT]")
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

        sync_to_async(print("channel_layer.group_discard"))

    async def receive(self, text_data):
        print("[RECEIVE]")
        print(f"RECEIVE >> text_data: {text_data}")
        text_data_json = json.loads(text_data)
        chat_user_id = text_data_json['chat_user_id']
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'chat_user_id': chat_user_id,
                'message': message
            }
        )

        await push_chat_notification(self.room_id, message, chat_user_id)

    async def chat_message(self, event):
        print("[CHAT_MESSAGE]")
        chat_user_id = event['chat_user_id']
        message = event['message']
        message_after_filter = return_bad_words_index(message, mode=0)

        user = ChatUser.objects.get(id=chat_user_id).user
        user = user.__dict__
        user['chat_user_id'] = chat_user_id
        print(f"CHAT_MESSAGE >> event: {event}")

        user['user_avatar'] = f"https://deliveryneighborsbucket.s3.ap-northeast-2.amazonaws.com/{user['avatar']}"
        serializers = ChattingUserSerializer(instance=user)
        print(f"CHAT_MESSAGE >> avatar: {user['avatar']}")
        print(f"CHAT_MESSAGE >> serializers: {serializers.data}")

        await self.send(text_data=json.dumps({
            'userInfo': serializers.data,
            'message': message_after_filter
        }, ensure_ascii=False
        ))


async def push_chat_notification(room_id, chat_message, sender_id):
    room = Room.objects.get(id=room_id)
    room_name = room.room_name
    chat_users = list(ChatUser.objects.filter(room=room))
    users = [chat_user.user for chat_user in chat_users if chat_user.user_id != sender_id]
    user_tokens = [user.fcm_token for user in users]
    print("채팅 fcm tokens", user_tokens)

    message = messaging.MulticastMessage(
        tokens=user_tokens,
        notification=messaging.Notification(
            title=f'{room_name}',
            body=f'{chat_message}'
        ),
        data={
            'title': f'{room_name}',
            'body': f'{chat_message}',
            'activity': 'waitingActivity'
        },
        # android=messaging.AndroidConfig(
        #     notification=messaging.AndroidNotification(
        #         click_action='waitingActivity'
        #     ),
        # ),
    )

    try:
        print("message 형태", message.data['activity'])
        response = messaging.send_multicast(message, dry_run=False)
        print("message send success")
        return Response({"status": status.HTTP_200_OK})
    except Exception as e:
        reason = e.__str__()
        print("푸시 알림 실패 원인", reason)
        return Response({"status": status.HTTP_400_BAD_REQUEST, "reason": reason})
