import requests
from rest_framework import serializers
from chat.models import Room, Category
from config.authentication import CustomJWTAuthentication


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'leader',
            'room_name',
            'created_at',
            'max_participant_num',
            'delivery_fee'
        ]


class RoomRetrieveSerializer(serializers.ModelSerializer):
    category_background_img = serializers.URLField(source='category.category_background_img')

    class Meta:
        model = Room
        fields = [
            'id',
            'leader',
            'room_name',
            'delivery_fee',
            'max_participant_num',
            'created_at',
            'pickup_address',
            'category_background_img'
        ]

# class CategoryCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['category_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
