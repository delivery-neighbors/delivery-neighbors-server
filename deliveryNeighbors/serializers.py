from rest_framework import serializers

from deliveryNeighbors.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'email', 'pwd', 'profile_img']
