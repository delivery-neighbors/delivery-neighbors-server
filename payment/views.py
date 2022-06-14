from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from config.settings.base import OPEN_BANK_CONFIG

# BASE_URL = "http://3.38.38.248/"  # deploy version
BASE_URL = "http://localhost:8000/"  # local version

OPENBANK_CLIENT_ID = OPEN_BANK_CONFIG['OPENBANK_API_KEY']
OPENBANK_REDIRECT_URI = f"{BASE_URL}{OPEN_BANK_CONFIG['OPENBANK_REDIRECT_URI']}"
OPENBANK_SECRET_KEY = OPEN_BANK_CONFIG['OPENBANK_SECRET_KEY']


@csrf_exempt
def openbank_authorize(request):
    authorize_api = "https://testapi.openbanking.or.kr/oauth/2.0/authorize?" \
                    "response_type={0}&client_id={1}&redirect_uri={2}" \
                    "&scope={3}&state={4}&auth_type={5}" \
        .format("code", OPENBANK_CLIENT_ID, OPENBANK_REDIRECT_URI,
                "login inquiry transfer", "b80BLsfigm9OokPTjy03elbJqRHOfGSY", "0")

    return redirect(authorize_api)

