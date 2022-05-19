import random
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy

from deliveryNeighbors.serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

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
        send_mail(mail_title, message, None, [mail_to], fail_silently=False)

        return JsonResponse({"message": "EMAIL SEND SUCCESS", "random_num": random_num})


class EmailVerifyView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerifySerializer

    def post(self, request):
        if request.data['email'] in authenticate_num_dict and authenticate_num_dict[request.data['email']] == \
                request.data['random_num']:
            authenticate_num_dict.pop(request.data['email'])
            return Response({"message": "EMAIL VERIFY SUCCESS", "email": request.data['email']})
        else:
            return Response({"message": "EMAIL VERIFY FAIL"})


class UserLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class

        request_email = request.data['email']
        request_password = request.data['password']

        user = User.objects.filter(email=request_email)

        if user:
            user_password = user[0].password
            if check_password(request_password, user_password):
                token = RefreshToken.for_user(user[0])
                refresh = str(token)
                access = str(token.access_token)

                return JsonResponse(
                    {"message": "USER LOGIN SUCCESS", 'user': user[0].pk, 'refresh': refresh, 'access': access})
            else:
                return Response("WRONG PASSWORD")
        else:
            return Response("USER NOT FOUND FOR THIS EMAIL")


class UserLogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response(
            {'message': "Successfully logged out"},
            status=status.HTTP_200_OK,
        )

        if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
            try:
                token = RefreshToken(request.data['refresh'])
                token.blacklist()

            except KeyError:
                response.data = {'message': "Refresh token was not included in request data"}
                response.status_code = status.HTTP_401_UNAUTHORIZED
            except (TokenError, AttributeError, TypeError) as error:
                if hasattr(error, 'args'):
                    if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                        response.data = {'message': gettext_lazy(error.args[0])}
                        response.status_code = status.HTTP_401_UNAUTHORIZED
                    else:
                        response.data = {'message': "An error has occurred"}
                        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                else:
                    response.data = {'message': "An error has occurred"}
                    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response
