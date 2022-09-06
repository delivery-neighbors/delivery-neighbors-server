from rest_framework import serializers

from accounts.models import User


class ChattingUserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='id')
    chat_user_id = serializers.CharField()
    user_avatar = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id', 'chat_user_id', 'username', 'user_avatar']
