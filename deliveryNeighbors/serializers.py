from rest_framework import serializers
from deliveryNeighbors.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_img']


class EmailSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField
    random_num = serializers.IntegerField


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
