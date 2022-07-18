import base64

import requests
from django.http import JsonResponse
from django.shortcuts import render

from config.settings.base import TOSS_PAYMENTS_CONFIG

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
