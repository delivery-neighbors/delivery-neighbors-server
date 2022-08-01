import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    room_group = []

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        # self.user_name = 'jiwoo'

    async def connect(self):
        print("connect")

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user_id = self.scope['url_route']['kwargs']['chat_user_id']

        self.group_name = 'chat_room_%s' % self.room_id
        print(self.group_name)

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )
        print(f"self.channel_name: {self.channel_name}")

        user = {self.user_id: self.channel_name}
        self.room_group.append({self.room_id: user})
        print("group", self.room_group)

        print("channel_layer.group_add")

        await self.accept()
        print("channel_layer.accept")

    async def disconnect(self, close_cod):
        print("disconnect")
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

        sync_to_async(print("channel_layer.group_discard"))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )
        sync_to_async(print("channel_layer.group_send"))

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

        sync_to_async(print("channel_layer.send"))
