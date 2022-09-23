from rest_framework import serializers

from neighbor.models import OrderFrequency


class OrderFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFrequency
        fields = '__all__'
