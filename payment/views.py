import base64

import requests
from django.http import JsonResponse
from requests import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView

from chat.models import ChatUser, Room
from config.settings.base import TOSS_PAYMENTS_CONFIG
from payment.models import Pay
from payment.serializers import PaySerializer

TOSS_API_KEY = TOSS_PAYMENTS_CONFIG['TOSS_API_KEY']
TOSS_SECRET_KEY = TOSS_PAYMENTS_CONFIG['TOSS_SECRET_KEY']


def payConfirmed(request):
    pay_api = "https://api.tosspayments.com/v1/payments/confirm"  # 결제 승인 api
    data_string = TOSS_SECRET_KEY + ":"
    str_bytes  = data_string.encode('utf-8')
    str_base64 = base64.b64encode(str_bytes)
    base64_str = str_base64.decode('utf-8')
    data = {
        "paymentKey": "5Z_AEEC420lbQO-KBs6zW", # payment
        "orderId": "mYVfEraupbFHZPAb",
        "amount": 15000
    }
    headers = {
        'Authorization': f"Basic {base64_str}",
        'Content-Type': 'application/json'
    }

    accept_response = requests.post(pay_api, data=data, headers=headers)
    accept_json = accept_response.json()
    return JsonResponse(accept_json)


class PayCreateListAPIView(ListCreateAPIView):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer

    def post(self, request, *args, **kwargs):
        chat_user = ChatUser.objects.get(id=kwargs['chatuser'])
        room = Room.objects.get(chatuser=chat_user)
        delivery_fee_1ps = int(room.delivery_fee / room.max_participant_num)  # 1인당 배달비
        print(delivery_fee_1ps)

        try:  # 이미 결제 정보를 생성했다면, 결제 정보 수정
            pay_obj = Pay.objects.get(order_id=chat_user)
            pay_obj.amount = int(request.data['amount']) + delivery_fee_1ps  # 자신의 주문금액 + 1인당 배달비
            pay_obj.save()

        except Pay.DoesNotExist:  # 없으면 결제 정보 생성
            Pay.objects.create(
                order_id=chat_user,
                amount=int(request.data['amount']) + delivery_fee_1ps
            )

        return JsonResponse({"status": status.HTTP_200_OK})

    def get(self, request, *args, **kwargs):
        chat_user = ChatUser.objects.get(id=kwargs['chatuser'])
        pay = Pay.objects.get(order_id=chat_user)

        pay = pay.__dict__
        pay['username'] = chat_user.user.username
        pay['room_name'] = Room.objects.get(chatuser=chat_user).room_name
        print(pay)

        serializer = PaySerializer(instance=pay)
        return JsonResponse({"status": status.HTTP_200_OK, "data": serializer.data})
