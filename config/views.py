import requests
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse
from django.shortcuts import redirect

from config.settings import SOCIAL_OAUTH_CONFIG
from deliveryNeighbors.models import User

KAKAO_CLIENT_ID = SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URI = SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI']
KAKAO_CLIENT_SECRET = SOCIAL_OAUTH_CONFIG['KAKAO_SECRET_KEY']


# Code Request
def kakao_login(request):
    url = "https://kauth.kakao.com/oauth/authorize?client_id={0}&redirect_uri={1}&response_type={2}"\
        .format(KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI, 'code')
    return redirect(url)


def kakao_callback(request):
    code = request.GET.get('code')  # 토큰 받기 요청에 필요한 인가 코드

    # Access Token Request
    token_api = "https://kauth.kakao.com/oauth/token"  # 토큰 받기 api
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "client_secret": KAKAO_CLIENT_SECRET,
        "code": code
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }

    token_response = requests.post(token_api, data=data, headers=headers)
    token_json = token_response.json()
    print(f"엑세스 토큰 가져오기 성공: {token_json}")  # <Response [200]>
    access_token = token_json['access_token']

    # Email Request
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    profile_json = profile_request.json()

    kakao_account = profile_json['kakao_account']
    email = kakao_account['email']

    # Signin, Sighup Request
    if not User.objects.filter(email=email).exists():
        # 유저 정보가 없으면 회원가입 되도록 합니다.
        user = User.objects.create(
            nickname=kakao_account['profile']['nickname'],
            email=email,
            pwd="kakao_default",
            profile_img=kakao_account['profile']['profile_image_url'],
        )

    print(f"user created: {email}")

    return JsonResponse({'access_token': access_token}, status=201)

