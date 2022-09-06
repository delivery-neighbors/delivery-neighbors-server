from rest_framework import serializers

from accounts.models import User
from neighbor.models import Review, UserReview, Address, Search


class UserSerializer(serializers.ModelSerializer):
    num_as_leader = serializers.IntegerField()
    num_as_participant = serializers.IntegerField()
    score = serializers.IntegerField()
    top3category = serializers.ListField(child=serializers.JSONField())

    class Meta:
        model = User
        fields = ['id', 'avatar', 'username', 'num_as_leader', 'num_as_participant', 'score', 'top3category']


class MyPageSerializer(serializers.ModelSerializer):
    num_as_leader = serializers.IntegerField()
    num_as_participant = serializers.IntegerField()
    score = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'avatar', 'username', 'num_as_leader', 'num_as_participant', 'score']


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
        fields = ['id', 'review', 'count']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'addr_latitude', 'addr_longitude']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar']


class UserSearchSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Search
        fields = ['id', 'search_content', 'created_at']


class UserIdCheckSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="id")

    class Meta:
        model = User
        fields = ['user_id']
