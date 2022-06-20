import requests
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from config.settings.base import OPEN_BANK_CONFIG

# BASE_URL = "http://3.38.38.248/"  # deploy version
BASE_URL = "http://localhost:8000/"  # local version

OPENBANK_CLIENT_ID = OPEN_BANK_CONFIG['OPENBANK_API_KEY']
OPENBANK_REDIRECT_URI = f"{BASE_URL}{OPEN_BANK_CONFIG['OPENBANK_REDIRECT_URI']}"
OPENBANK_SECRET_KEY = OPEN_BANK_CONFIG['OPENBANK_SECRET_KEY']
OPENBANK_STATE = OPEN_BANK_CONFIG['OPENBANK_STATE']


@csrf_exempt
def openbank_authorize(request):
    authorize_api = "https://testapi.openbanking.or.kr/oauth/2.0/authorize?" \
                    "response_type={0}&client_id={1}&redirect_uri={2}" \
                    "&scope={3}&state={4}&auth_type={5}" \
        .format("code", OPENBANK_CLIENT_ID, OPENBANK_REDIRECT_URI,
                "login inquiry transfer", OPENBANK_STATE, "0")

    return redirect(authorize_api)


def openbank_callback(request):
    code = request.GET.get('code')  # 토큰 받기 요청에 필요한 인가 코드
    print(f"인가 코드: {code}")

    # 토큰 발급 api
    token_api = "https://testapi.openbanking.or.kr/oauth/2.0/token"
    data = {
        "code": code,
        "client_id": OPENBANK_CLIENT_ID,
        "client_secret": OPENBANK_SECRET_KEY,
        "redirect_uri": OPENBANK_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    token_response = requests.post(token_api, data=data, headers=headers)
    token_json = token_response.json()

    #
    account_api = "https://testapi.openbanking.or.kr/oauth/2.0/authorize_account" \
                  "?response_type={0}&client_id={1}&redirect_uri={2}&scope={3}" \
                  "&client_info={4}&state={5}&auth_type={6}" \
                  .format("code", OPENBANK_CLIENT_ID, OPENBANK_REDIRECT_URI, "login inquiry transfer"
                          , "test", OPENBANK_STATE, "0")

    return redirect(account_api)

    # return JsonResponse(token_json)
