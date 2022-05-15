import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import status

from config.settings import SOCIAL_OAUTH_CONFIG
from deliveryNeighbors.models import User

BASE_URL = "http://localhost:8070/"

KAKAO_CLIENT_ID = SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URI = SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI']
KAKAO_CLIENT_SECRET = SOCIAL_OAUTH_CONFIG['KAKAO_SECRET_KEY']


# Code Request
def kakao_login(request):
    url = "https://kauth.kakao.com/oauth/authorize?client_id={0}&redirect_uri={1}&response_type={2}"\
        .format(KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI, 'code')
    return redirect(url)


# kakao Signin or Signup
def kakao_callback(request):
    code = request.GET.get('code')  # 토큰 받기 요청에 필요한 인가 코드
    print(f"인가 코드: {code}")

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
    access_token = token_json['access_token']
    print(f"엑세스 토큰 가져오기 성공: {access_token}")

    # Email Request
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    profile_json = profile_request.json()

    kakao_account = profile_json['kakao_account']

    email = kakao_account['email']
    uid = profile_json['id']

    # Login, Sighup Request
    try:
        # 로그인
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        if not social_user:  # 소셜 로그인이 아닐 경우
            return JsonResponse(
                {"error_message": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "kakao":  # kakao 소셜 로그인이 아닌 경우
            return JsonResponse(
                {"error_message": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # kakao 유저 로그인
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse(
                {"error_message": "failed to signin"}, status=accept_status
            )
        accept_json = accept.json()
        accept_json.pop("user", None)
        print("kakao 로그인 성공!")
        return JsonResponse(accept_json)

    except User.DoesNotExist:
        # 기존에 가입한 유저가 아니면 회원 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data
        )
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse(
                {"error_message": f"failed to signup, {accept_status}"}, status=accept_status
            )
        accept_json = accept.json()
        accept_json.pop("user", None)
        print("kakao 회원 가입")
        return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_REDIRECT_URI


def kakao_logout(request):
    print("로그아웃")
    logout_kakao_uri = "https://kapi.kakao.com/v1/user/logout"
    access_token = request.session.get('access_token')
    print(access_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    accept = requests.post(logout_kakao_uri, headers=headers)
    # 로그아웃 에러 예외 처리 status_code
    accept_status = accept.status_code
    if accept_status != 200:
        return JsonResponse(
            {"error_message": f"failed to logout, {accept_status}"}, status=accept_status
        )

    return JsonResponse(accept.json())
