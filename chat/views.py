from rest_framework.generics import *
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

import config.authentication
from accounts.models import User
from chat.models import Category, Room
from chat.serializers import CategoryListSerializer, RoomListSerializer, RoomRetrieveSerializer
from config.authentication import CustomJWTAuthentication


class RoomGetCreateAPIView(ListCreateAPIView):
    def get(self, request):
        queryset = Room.objects.all()
        serializer = RoomListSerializer(instance=queryset, many=True)
        return Response(serializer.data)

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


class RoomGetDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomRetrieveSerializer

    def get(self, request, *args, **kwargs):
        # path-variable <int:pk> 정보를 통해 해당 id의 room 객체 get
        room = self.get_object()

        # RoomRetrieveSerializer 이용해
        serializer = self.serializer_class
        # retrieve()
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = CustomJWTAuthentication.authenticate(self, request)
        print("user", user)
        room = self.get_object()
        room_leader = room.leader.pk
        print("room leader", room_leader)

        # 채팅방 leader 와  로그인 유저가 같으면 삭제 가능
        if user == room_leader:
            self.destroy(request, *args, **kwargs)
            return Response(status=status.HTTP_200_OK)

        else:
            # 다르면 401 UNAUTHORIZED 에러 응답
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# class CategoryCreateView(CreateAPIView):
#     serializer_class = CategoryCreateSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
