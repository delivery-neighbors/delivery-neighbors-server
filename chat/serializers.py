import requests
from rest_framework import serializers
from chat.models import Room, Category
from config.authentication import CustomJWTAuthentication


# 채팅방 목록(메인 화면) serializer
class RoomListSerializer(serializers.ModelSerializer):
    distance = serializers.IntegerField()
    leader_avatar = serializers.URLField(source='leader.avatar')
    participant_num = serializers.IntegerField()

    class Meta:
        model = Room
        fields = [
            'id',
            'leader',
            'leader_avatar',
            'room_name',
            'created_at',
            'participant_num',
            'max_participant_num',
            'delivery_fee',
            'distance'
        ]


# 채팅방 정보 serializer
class RoomRetrieveSerializer(serializers.ModelSerializer):
    category_background_img = serializers.URLField(source='category.category_background_img')
    leader_avatar = serializers.URLField(source='leader.avatar')
    participant_num = serializers.IntegerField()

    class Meta:
        model = Room
        fields = [
            'id',
            'leader',
            'leader_avatar',
            'room_name',
            'delivery_fee',
            'participant_num',
            'max_participant_num',
            'created_at',
            'pickup_address',
            'category_background_img'
        ]


# 카테고리 serializer
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
