from rest_framework import serializers

from accounts.models import User
from chatting.models import Message


class ChattingUserSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField()
    user_id = serializers.CharField(source='id')
    chat_user_id = serializers.CharField()
    user_avatar = serializers.CharField()

    class Meta:
        model = User
        fields = ['room_id', 'user_id', 'chat_user_id', 'username', 'user_avatar']


class MessageListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='chat_user.user.id')
    username = serializers.CharField(source='chat_user.user.username')
    user_avatar = serializers.CharField()

    class Meta:
        model = Message
        fields = ['id', 'user_id', 'chat_user', 'username', 'user_avatar', 'message']
