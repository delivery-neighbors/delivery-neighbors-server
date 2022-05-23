import requests
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

import config.authentication
from accounts.models import User
from chat.models import Category, Room
from chat.serializers import CategoryListSerializer
from config.authentication import CustomJWTAuthentication


class RoomCreateAPIView(APIView):
    def post(self, request):
        # request 에서 user_id 추출
        leader = CustomJWTAuthentication.authenticate(self, request)
        print("user", leader)

        # 요청 받은 category id로 해당 카테고리 객체 get
        cate_id = request.data['category']
        print("cate_id", cate_id)
        category = Category.objects.get(id=cate_id)
        print("category type", type(category))
        print("category", category)

        Room.objects.create(
            leader=User.objects.get(id=leader),
            room_name=request.data['room_name'],
            category=Category.objects.get(id=cate_id),
            delivery_platform=request.data['delivery_platform'],
            delivery_fee=request.data['delivery_fee'],
            max_participant_num=request.data['max_participant_num'],
            pickup_address=request.data['pickup_address'],
            pickup_latitude=request.data['pickup_latitude'],
            pickup_longitude=request.data['pickup_longitude']
        )

        return Response(status=status.HTTP_201_CREATED)


# class CategoryCreateView(CreateAPIView):
#     serializer_class = CategoryCreateSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
