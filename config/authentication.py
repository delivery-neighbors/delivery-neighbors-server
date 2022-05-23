import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from accounts.models import User


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            if token is None:
                return None

            pre_jwt, jwt_token = token.split(' ')
            decoded = jwt.decode(jwt_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

            return decoded['user_id']

        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(default='JWT Format Invalid')
