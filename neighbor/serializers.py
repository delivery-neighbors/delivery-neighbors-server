from rest_framework import serializers

from accounts.models import User
from neighbor.models import Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'avatar', 'date_joined', 'last_login', 'is_active']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
