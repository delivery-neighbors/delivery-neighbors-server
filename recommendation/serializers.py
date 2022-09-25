from rest_framework import serializers

from chat.models import Room
from neighbor.models import OrderFrequency


class OrderFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFrequency
        fields = '__all__'


class SimilarUserChatroomSerializer(serializers.ModelSerializer):
    distance = serializers.IntegerField()
    leader_avatar = serializers.ImageField(source='leader.avatar')
    participant_num = serializers.IntegerField()

    class Meta:
        model = Room
        fields = [
            'id',
            'leader_avatar',
            'room_name',
            'created_at',
            'participant_num',
            'max_participant_num',
            'delivery_fee',
            'distance',
            'status'
        ]
