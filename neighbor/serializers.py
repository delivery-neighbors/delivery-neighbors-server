from rest_framework import serializers

from accounts.models import User
from neighbor.models import Review, UserReview, Address, Search


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'avatar', 'date_joined', 'last_login', 'is_active']


class ReviewSerializer(serializers.Serializer):
    reviewList = serializers.ListField(child=serializers.CharField())


class ReviewRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class UserReviewSerializer(serializers.ModelSerializer):
    review = serializers.CharField(source='review_id.content')

    class Meta:
        model = UserReview
        fields = ['review', 'count']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['addr_latitude', 'addr_longitude']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar']


class UserSearchSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Search
        fields = ['search_content', 'created_at']
