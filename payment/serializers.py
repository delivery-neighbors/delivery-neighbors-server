from rest_framework import serializers

from payment.models import Pay


class PaySerializer(serializers.ModelSerializer):
    room_name = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = Pay
        fields = ['username', 'room_name', 'order_id', 'amount']
