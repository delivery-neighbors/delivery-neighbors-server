import requests
from rest_framework import serializers
from chat.models import Room, Category, Location, ChatUser
from config.authentication import CustomJWTAuthentication


# 채팅방 목록(메인 화면) serializer
from payment.models import Pay


class RoomListSerializer(serializers.ModelSerializer):
    distance = serializers.IntegerField()
    is_leader = serializers.BooleanField()
    leader_avatar = serializers.ImageField(source='leader.avatar')
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
            'distance',
            'status'
        ]


# 채팅방 정보 serializer
class RoomRetrieveSerializer(serializers.ModelSerializer):
    category_background_img = serializers.URLField(source='category.category_background_img')
    leader_name = serializers.CharField(source='leader.username')
    leader_avatar = serializers.ImageField(source='leader.avatar')
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
    leader_avatar = serializers.ImageField(source='leader.avatar')
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
    user_avatar = serializers.ImageField(source='user.avatar')
    review_status = serializers.IntegerField()

    class Meta:
        model = ChatUser
        fields = ['id', 'user', 'username', 'user_avatar', 'review_status']


class CurLocationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Location
        fields = ['user', 'username', 'cur_latitude', 'cur_longitude']


class ChatUserStatusSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    chatuser_id = serializers.IntegerField(source='id')
    name = serializers.CharField(source='user.username')
    user_avatar = serializers.ImageField(source='user.avatar')
    status = serializers.BooleanField()

    class Meta:
        model = ChatUser
        fields = ['user_id', 'chatuser_id', 'name', 'user_avatar', 'status']


class MyInfoByRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_name', 'status']


class PickupLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['pickup_address', 'pickup_latitude', 'pickup_longitude']


class ChatUserPayInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    user_avatar = serializers.ImageField()
    amount = serializers.IntegerField()

    class Meta:
        model = Pay
        fields = ['id', 'username', 'user_avatar', 'amount']
