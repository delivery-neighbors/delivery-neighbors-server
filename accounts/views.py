import base64
import random

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

from config.authentication import CustomJWTAuthentication
from neighbor.models import UserReliability, OrderFrequency

from config.settings.base import SOCIAL_OAUTH_CONFIG

BASE_URL = "https://baedalius.com/"  # deploy version
# BASE_URL = "http://localhost:8000/"  # local version

KAKAO_CLIENT_ID = SOCIAL_OAUTH_CONFIG['KAKAO_REST_API_KEY']
KAKAO_REDIRECT_URI = f"{BASE_URL}{SOCIAL_OAUTH_CONFIG['KAKAO_REDIRECT_URI']}"
KAKAO_CLIENT_SECRET = SOCIAL_OAUTH_CONFIG['KAKAO_SECRET_KEY']

authenticate_num_dict = {}


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        avatar = request.FILES.getlist('avatar')

        # fcm token
        fcm_token = request.data['fcm']

        if avatar:
            user_data = {
                'username': username,
                'email': email,
                # 'password': make_password(request.data['password']),
                'password': make_password(password),
                'avatar': avatar[0],
                'fcm_token': fcm_token
            }

        else:
            user_data = {
                'username': request.data['username'],
                'email': email,
                'password': make_password(password),
                'fcm_token': fcm_token
            }

        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=False):
            # 유저 생성과 함께 토큰 발급
            user = serializer.create(user_data)
            user_reliability = UserReliability.objects.create(user=user)
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            # 유저 생성 시 유저 주문 빈도 정보를 담고 있는 OrderFrequency 행 생성
            user_order_frequency = OrderFrequency.objects.create(user=user)

        else:
            print(serializer.errors)
            return Response({"status": status.HTTP_400_BAD_REQUEST})

        # 아바타가 있으면 이미지 저장
        # if avatar:
        #     imgdata = base64.b64decode(avatar)
        #     with open(f"media/images/avatar/{email}-avatar.jpg", 'wb') as f:
        #         f.write(imgdata)
        #
        #     user = User.objects.get(email=email)
        #     user.avatar = f"images/avatar/{email}-avatar.jpg"
        #     user.save()

        return JsonResponse(
            {"status": status.HTTP_201_CREATED, "user": user.pk, "access": access, "refresh": refresh})


class EmailSendView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSendSerializer

    def post(self, request):
        random_num = int(random.random() * 1000000)
        print("random_num", random_num)
        message = f"회원가입을 위해 아래의 난수를 확인 창에 입력하세요.\n{random_num}"

        authenticate_num_dict[request.data['email']] = random_num

        mail_title = "회원가입을 위해 이메일을 인증하세요"
        mail_to = request.data['email']
        send_mail(mail_title, message, None, [mail_to], fail_silently=False)

        return JsonResponse({"status": status.HTTP_200_OK, "data": {"random_num": random_num}})


class EmailVerifyView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerifySerializer

    def post(self, request):
        if request.data['email'] in authenticate_num_dict and \
                authenticate_num_dict[request.data['email']] == request.data['random_num']:
            authenticate_num_dict.pop(request.data['email'])
            return Response({"status": status.HTTP_200_OK, "data": {"email": request.data['email']}})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


class UserLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class

        request_email = request.data['email']
        request_password = request.data['password']

        # fcm token
        fcm_token = request.data['fcm']

        try:
            user = User.objects.get(email=request_email)  # 여기서 객체가 없으면 DoesNotExist 예외처리
            user_password = user.password
            if check_password(request_password, user_password):
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)

                user.fcm_token = fcm_token
                user.save()

                return JsonResponse({"status": status.HTTP_200_OK,
                                     "user": user.pk, "refresh": refresh, "access": access})  # 성공메세지
            else:
                return JsonResponse(
                    {"status": status.HTTP_400_BAD_REQUEST})  # 에러메세지

        except User.DoesNotExist:
            return JsonResponse(
                {"status": status.HTTP_401_UNAUTHORIZED})  # 에러메세지 2


class UserLogoutAPIView(APIView):
    def post(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)
        user = User.objects.get(id=user_id)

        response = Response({"status": status.HTTP_200_OK})

        if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
            try:
                token = RefreshToken(request.data['refresh'])
                token.blacklist()

                # fcm token delete
                user.fcm_token = None
                user.save()

            except KeyError:
                response.data = {"status": status.HTTP_400_BAD_REQUEST}
                response.status_code = status.HTTP_401_UNAUTHORIZED
            except (TokenError, AttributeError, TypeError) as error:
                if hasattr(error, 'args'):
                    if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                        response.data = {"status": status.HTTP_401_UNAUTHORIZED}
                    else:
                        response.data = {"status": status.HTTP_500_INTERNAL_SERVER_ERROR}
                else:
                    response.data = {"status": status.HTTP_500_INTERNAL_SERVER_ERROR}
        return response


class UserResignAPIView(APIView):
    def delete(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        user = User.objects.get(id=user_id)
        user.delete()

        return Response({"status": status.HTTP_200_OK})


class PwdResetAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        request_email = request.data['email']
        request_password = request.data['password']

        user = User.objects.get(email=request_email)
        user.set_password(request_password)
        user.save()

        return Response({"status": status.HTTP_200_OK})

# Code Request
@csrf_exempt
def kakao_login(request):
    url = "https://kauth.kakao.com/oauth/authorize?client_id={0}&redirect_uri={1}&response_type={2}" \
        .format(KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI, 'code')
    return redirect(url)


# kakao Login or Signup
@csrf_exempt
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

    # session 저장
    request.session['access_token'] = access_token
    request.session['client_id'] = KAKAO_CLIENT_ID
    request.session['redirect_uri'] = KAKAO_REDIRECT_URI

    # Email Request
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    profile_json = profile_request.json()
    kakao_account = profile_json['kakao_account']
    kakao_profile = kakao_account['profile']
    email = kakao_account['email']

    # Login, Sighup Request
    try:
        # 로그인
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.filter(user=user)

        if not social_user:  # 소셜 로그인이 아닐 경우 (자체로그인)
            return JsonResponse({"status": status.HTTP_404_NOT_FOUND})
        if social_user[0].provider != "kakao":  # kakao 소셜 로그인이 아닌 경우
            return JsonResponse({"status": status.HTTP_400_BAD_REQUEST})

        # kakao 유저 로그인
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse(
                {"status": accept_status})
        accept_json = accept.json()
        accept_json.pop("user", None)

        user = User.objects.get(email=email)
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        print("kakao 로그인 성공!")

        return JsonResponse({"status": status.HTTP_200_OK, "data": accept_json})

    except User.DoesNotExist:
        # 기존에 가입한 유저가 아니면 회원 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data
        )
        # 프로필 사진 설정
        user = User.objects.get(email=email)
        avatar_url = kakao_profile['profile_image_url']

        # 카카오 기본 사진이 아닐 때 -> 이미지 저장
        if avatar_url != "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg":
            avatar_request = requests.get(avatar_url)
            user.avatar.save(
                f"{kakao_account['email']}.jpg", ContentFile(avatar_request.content)
            )
        else:  # 기본 이미지일 때 -> 저장된 이미지 적용
            user.avatar = "media/avatar/default_img.jpg"
        user.save()

        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"status": accept_status})
        accept_json = accept.json()
        accept_json.pop("user", None)

        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        print("kakao 회원 가입 성공!")

        return JsonResponse({"status": status.HTTP_200_OK, "data": accept_json})


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_REDIRECT_URI


@csrf_exempt
def kakao_logout(request):
    if request.user.is_authenticated:
        print(f"현재 로그 아웃할 유저: {request.user.username}")

    access_token = request.session['access_token']
    accept = requests.post(
        "https://kapi.kakao.com/v1/user/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # 로그아웃 에러 예외 처리 status_code
    accept_status = accept.status_code
    if accept_status != 200:
        return JsonResponse({"status": accept_status}, status=accept_status)
    auth.logout(request)

    return JsonResponse({"status": status.HTTP_200_OK, "data": accept.json()})
