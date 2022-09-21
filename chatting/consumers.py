import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import User
from ai.cleanbot.cleanbot import return_bad_words_index
from chat.models import ChatUser
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
