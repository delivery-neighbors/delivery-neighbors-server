import requests
from rest_framework import serializers
from chat.models import Room, Category
from config.authentication import CustomJWTAuthentication


# serializer 사용 안 하고 objects.create()로 생성
# class RoomCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = ['leader',
#                   'room_name',
#                   'category',
#                   'delivery_platform',
#                   'delivery_fee',
#                   'max_participant_num',
#                   'pickup_address',
#                   'pickup_latitude',
#                   'pickup_longitude']


# class CategoryCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['category_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
