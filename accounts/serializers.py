from rest_framework import serializers
from accounts.models import User, Address


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'avatar']


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


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['addr_latitude', 'addr_longitude']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar']
