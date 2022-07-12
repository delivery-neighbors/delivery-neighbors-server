import requests
from rest_framework import serializers
from chat.models import Room, Category, Location, ChatUser
from config.authentication import CustomJWTAuthentication


# 채팅방 목록(메인 화면) serializer
class RoomListSerializer(serializers.ModelSerializer):
    distance = serializers.IntegerField()
    is_leader = serializers.BooleanField()
    leader_avatar = serializers.URLField(source='leader.avatar')
    participant_num = serializers.IntegerField()

    class Meta:
        model = Room
        fields = [
            'id',
            'is_leader',
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
    leader_name = serializers.CharField(source='leader.username')
    leader_avatar = serializers.URLField(source='leader.avatar')
    participant_num = serializers.IntegerField()

    class Meta:
        model = Room
        fields = [
            'id',
            'leader_name',
            'leader_avatar',
            'room_name',
            'delivery_fee',
            'participant_num',
            'max_participant_num',
            'created_at',
            'pickup_address',
            'category_background_img'
        ]


# class RoomJoinedSerializer(serializers.ModelSerializer):
#     is_leader = serializers.BooleanField()
#     leader_avatar = serializers.URLField(source='leader.avatar')
#     participant_num = serializers.IntegerField()
#
#     class Meta:
#         model = Room
#         fields = [
#             'id',
#             'is_leader',
#             'leader_avatar',
#             'room_name',
#             'created_at',
#             'participant_num',
#             'max_participant_num',
#             'delivery_fee',
#         ]


class RoomDoneSerializer(serializers.ModelSerializer):
    is_leader = serializers.BooleanField()
    leader_avatar = serializers.URLField(source='leader.avatar')
    participant_num = serializers.IntegerField()
    review_status = serializers.BooleanField()

    class Meta:
        model = Room
        fields = [
            'id',
            'is_leader',
            'leader_avatar',
            'room_name',
            'participant_num',
            'max_participant_num',
            'review_status',
        ]

# 카테고리 serializer
# class CategoryListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'


class ChatUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    user_avatar = serializers.URLField(source='user.avatar')

    class Meta:
        model = ChatUser
        fields = ['id', 'user', 'username', 'user_avatar']


class CurLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['user', 'cur_latitude', 'cur_longitude']
