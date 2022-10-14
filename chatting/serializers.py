from rest_framework import serializers

from accounts.models import User


class ChattingUserSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField()
    user_id = serializers.CharField(source='id')
    chat_user_id = serializers.CharField()
    user_avatar = serializers.CharField()

    class Meta:
        model = User
        fields = ['room_id', 'user_id', 'chat_user_id', 'username', 'user_avatar']
