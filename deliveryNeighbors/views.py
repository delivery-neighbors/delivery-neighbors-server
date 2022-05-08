from io import BytesIO
from django.views import View
from rest_framework import status
from rest_framework.generics import *
from rest_framework.parsers import JSONParser

import deliveryNeighbors.models
from deliveryNeighbors.models import *
from deliveryNeighbors.serializers import *
from rest_framework.response import Response


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    print("queryset", queryset)
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        print("request", data)
        encrypted_pwd = data['pwd'] + '//'
        print(encrypted_pwd)

        user_data = {
            'nickname': data['nickname'],
            'email': data['email'],
            'pwd': encrypted_pwd,
            'profile_img': data['profile_img']
        }
        print("user_data", user_data)
        serializer = self.get_serializer(data=user_data, context={'request': request})

        if serializer.is_valid():
            new_user = User(**serializer.validated_data)
            new_user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
