import random

from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode
from django.views import View
from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from deliveryNeighbors.serializers import *
from rest_framework.response import Response

authenticate_num_dict = {}


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if request.data['profile_img']:
            user_data = {
                'username': request.data['username'],
                'email': request.data['email'],
                'password': make_password(request.data['password']),
                'profile_img': request.data['profile_img']
            }
        else:
            user_data = {
                'username': request.data['username'],
                'email': request.data['email'],
                'password': make_password(request.data['password'])
            }

        if serializer.is_valid(raise_exception=False):
            user = serializer.create(user_data)
            print("user", user)
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse(
                {"message": "USER CREATE SUCCESS", 'user': user.pk, 'access': access, 'refresh': refresh})

        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
        email = EmailMessage(mail_title, message, to=[mail_to])
        email.send()

        return JsonResponse({"message": "EMAIL SEND SUCCESS", "random_num": random_num})


class EmailVerifyView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerifySerializer

    def post(self, request):
        if request.data['email'] in authenticate_num_dict and authenticate_num_dict[request.data['email']] == request.data['random_num']:
            authenticate_num_dict.pop(request.data['email'])
            return Response({"message": "EMAIL VERIFY SUCCESS", "email": request.data['email']})
        else:
            return Response({"message": "EMAIL VERIFY FAIL"})

# class UserLoginAPIView(GenericAPIView):
#     # serializer_class = UserLoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             response = {
#                 "success": "True",
#                 "status_code": status.HTTP_200_OK,
#                 "message": "user login success",
#                 "token": serializer.data['token']
#             }
#
#         return Response(response)


# "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyNjQ1MDI2LCJpYXQiOjE2NTI2MzQyMjYsImp0aSI6Ijg5NjQ0NDY4MTFmMzQyMDlhYzJiMTdiZmIyNzY4MzMyIiwidXNlcl9pZCI6M30.NrS3CQTpSoM3qUzI5WSfexo4A6cLoMEbQnaI3QHlluU"
