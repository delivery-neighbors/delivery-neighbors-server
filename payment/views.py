import base64
from datetime import datetime
from random import randint

import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from chat.models import ChatUser, Room
from config.settings.base import TOSS_PAYMENTS_CONFIG
from payment.models import Pay
from payment.serializers import PaySerializer

TOSS_API_KEY = TOSS_PAYMENTS_CONFIG['TOSS_API_KEY']
TOSS_SECRET_KEY = TOSS_PAYMENTS_CONFIG['TOSS_SECRET_KEY']


class PayCreateListAPIView(ListCreateAPIView):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer

    def post(self, request, *args, **kwargs):
        chat_user = ChatUser.objects.get(id=kwargs['chatuser'])
        room = Room.objects.get(chatuser=chat_user)
        delivery_fee_1ps = int(room.delivery_fee / room.max_participant_num)  # 1인당 배달비

        order_id = f"Dn-{datetime.now().strftime('%Y%m%d%H%M')}_{randint(1000, 9999)}"

        try:  # 이미 결제 정보를 생성했다면, 결제 정보 수정
            pay_obj = Pay.objects.get(chat_user=chat_user)
            pay_obj.amount = int(request.data['amount']) + delivery_fee_1ps  # 자신의 주문금액 + 1인당 배달비
            pay_obj.save()

        except Pay.DoesNotExist:  # 없으면 결제 정보 생성
            Pay.objects.create(
                chat_user=chat_user,
                order_id = order_id,
                amount=int(request.data['amount']) + delivery_fee_1ps
            )

        # 채팅 유저의 상태값 변경
        chat_user.status = 'CONFIRMED'
        chat_user.save()

        # 결제 정보를 모두 입력되면, 방의 상태를 변경
        chat_users_confirmed_with_room = ChatUser.objects.filter(room=room, status="CONFIRMED")
        if len(chat_users_confirmed_with_room) == room.max_participant_num:
            room.status = "CONFIRMED"
            room.save()

        return JsonResponse({"status": status.HTTP_200_OK})

    def get(self, request, *args, **kwargs):
        chat_user = ChatUser.objects.get(id=kwargs['chatuser'])
        pay = Pay.objects.get(chat_user=chat_user)

        pay = pay.__dict__
        pay['username'] = chat_user.user.username
        pay['room_name'] = Room.objects.get(chatuser=chat_user).room_name

        serializer = PaySerializer(instance=pay)
        return JsonResponse({"status": status.HTTP_200_OK, "data": serializer.data})


def PayConfirmed(request):
    response_orderId = request.GET["orderId"]
    response_paymentKey = request.GET["paymentKey"]
    response_amount = int(request.GET["amount"])

    # 결제 승인 api
    pay_api = "https://api.tosspayments.com/v1/payments/confirm"
    data_string = TOSS_SECRET_KEY + ":"
    str_bytes = data_string.encode('utf-8')
    str_base64 = base64.b64encode(str_bytes).decode()

    data = {
        "paymentKey": response_paymentKey,  # payment
        "orderId": response_orderId,
        "amount": response_amount
    }
    headers = {
        'Authorization': f"Basic {str_base64}",
        'Content-Type': 'application/json'
    }

    accept_response = requests.post(pay_api, json=data, headers=headers)
    accept_json = accept_response.json()
    print(f"결제 완료 resopnse: {accept_json}")

    # 결제 요청한 금액과 결제된 금액이 일치하는지 확인
    success_response_amount = int(accept_json['card']['amount'])
    request_user_amount = Pay.objects.get(order_id=response_orderId).amount

    if success_response_amount != request_user_amount:
        return JsonResponse({"status": status.HTTP_406_NOT_ACCEPTABLE})

    # 채팅 유저 상태 변경
    chat_user = Pay.objects.get(order_id=response_orderId).chat_user
    print(type(chat_user))
    # chat_user = ChatUser.objects.get(id=chat_user_id)
    # print(chat_user)
    chat_user.status = 'PAY_DONE'  # 객체라면 통과
    chat_user.save()

    # 채팅방 상태 변경 (방장을 제외한 채팅 유저들이 모두 'PAY_DONE' 상태일 때)
    participated_room = chat_user.room
    chat_user_pay_done = ChatUser.objects.filter(room=participated_room, status='PAY_DONE')
    if len(chat_user_pay_done) == participated_room.max_participant_num - 1:
        participated_room.status = 'PAY_DONE'
        participated_room.save()

    return JsonResponse({"status": status.HTTP_200_OK})


def PayFailed(request):
    return JsonResponse({"status": status.HTTP_402_PAYMENT_REQUIRED})