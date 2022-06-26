from datetime import timedelta, datetime

from django.db.models import Q
from django.http import JsonResponse
from rest_framework.filters import SearchFilter
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status, filters, request

from accounts.models import User
from chat.models import Category, Room, ChatUser, Location
from chat.serializers import RoomListSerializer, RoomRetrieveSerializer, CurLocationSerializer, ChatUserSerializer
from config.authentication import CustomJWTAuthentication

from haversine import haversine, Unit


class RoomGetCreateAPIView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer

    def get(self, request):
        category_id = request.GET['category_id']

        request_latitude = float(request.GET['user_latitude'])
        request_longitude = float(request.GET['user_longitude'])
        request_location = (request_latitude, request_longitude)
        request_search = request.GET['search']

        # filter()에 넣어줄 조건
        # 1km에 대해 위도는 0.01 차이, 경도는 0.015 차이
        # 즉, request 통해 받아온 위치(위도,경도)에서 +,- 0.005 (위도) / +,- 0.0075 (경도) 떨어진 곳까지 1차 필터링
        # Q 클래스 -> filter()에 넣어줄 논리 조건을 | 또는 & 사용해 조합 가능케 해줌
        condition = (
                Q(pickup_latitude__range=(request_latitude - 0.005, request_latitude + 0.005)) &
                Q(pickup_longitude__range=(request_longitude - 0.0075, request_longitude + 0.0075)) &
                Q(room_name__contains=request_search)
        )
        rooms_first_filtering = Room.objects.filter(condition)

        # 500m 이내 채팅방 2차 필터링
        rooms_within_500meters = [room for room in rooms_first_filtering
                                  if haversine(request_location,
                                               (room.pickup_latitude, room.pickup_longitude),
                                               unit=Unit.METERS) < 500]

        if category_id:
            category = Category.objects.get(id=category_id)
            rooms_by_category = [room for room in rooms_within_500meters
                                 if room.category == category]
        else:
            rooms_by_category = rooms_within_500meters
        print("rooms_by_category", rooms_by_category)

        for room in rooms_by_category:
            room_id = room.id

            # created_at 가공
            now = datetime.now()
            created_at = room.created_at

            if now - created_at >= timedelta(days=7):
                # strftime() -> datetime 형식화 메소드
                # %b -> 달을 짧게 출력, %d -> 날 출력
                room.created_at = created_at.strftime("%b %d")

            elif now - created_at >= timedelta(days=1):
                # %a 옵션 -> datetime 객체의 요일을 짧게 출력
                room.created_at = created_at.strftime("%a")

            else:
                # %H -> 시간을 0~23 사용해 출력, %M -> 분 출력
                room.created_at = created_at.strftime("%H:%M")

            # 1인당 배달비 계산
            delivery_fee = room.delivery_fee
            max_participant_num = room.max_participant_num
            del_fee_for_person = int(delivery_fee / max_participant_num)
            room.delivery_fee = del_fee_for_person

            # 거리 계산
            distance = haversine(request_location, (room.pickup_latitude, room.pickup_longitude), unit=Unit.METERS)

            # 현재 채팅방 참여자 수 추출
            participant_num = ChatUser.objects.filter(room_id=room_id).count()

            # 거리, 현재 채팅방 참여자 수 정보 추가를 위해 room 객체를 dict 로 변환 뒤
            # 해당 dict 에 participant_num key-value 추가
            room = room.__dict__
            room['distance'] = int(distance)
            room['participant_num'] = participant_num

        serializer = RoomListSerializer(instance=rooms_by_category, many=True)
        return Response(serializer.data)

    def post(self, request):
        # request 에서 user_id 추출
        leader = CustomJWTAuthentication.authenticate(self, request)
        print("------------------------------------")
        print("RoomCreate", leader, "번 유저가 채팅방 생성")

        # 요청 받은 category id로 해당 카테고리 객체 get
        cate_id = request.data['category']
        category = Category.objects.get(id=cate_id)

        room = Room.objects.create(
            leader=User.objects.get(id=leader),
            room_name=request.data['room_name'],
            category=category,
            delivery_platform=request.data['delivery_platform'],
            delivery_fee=request.data['delivery_fee'],
            max_participant_num=request.data['max_participant_num'],
            pickup_address=request.data['pickup_address'],
            pickup_latitude=request.data['pickup_latitude'],
            pickup_longitude=request.data['pickup_longitude']
        )

        ChatUser.objects.create(
            room=room,
            user=User.objects.get(id=leader)
        )

        return Response(status=status.HTTP_201_CREATED)


class RoomRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomRetrieveSerializer

    def get(self, request, *args, **kwargs):
        # path-variable <int:pk> 정보를 통해 해당 id의 room 객체 get
        room = self.get_object()
        room_id = room.pk

        # created_at 가공
        created_at = room.created_at
        room.created_at = created_at.strftime("%Y.%m.%d")

        # 1인당 배달비 계산
        delivery_fee = room.delivery_fee
        max_participant_num = room.max_participant_num
        del_fee_for_person = int(delivery_fee / max_participant_num)
        room.delivery_fee = del_fee_for_person

        # 현재 채팅방 참여자 수 추출
        participant_num = ChatUser.objects.filter(room_id=room_id).count()
        # 현재 채팅방 참여자 수 정보 추가를 위해 room 객체를 dict 로 변환 뒤
        participant_detail = room.__dict__
        # 해당 dict 에 participant_num key-value 추가
        # -> room 객체에 participant_num 정보 자동 삽입
        participant_detail['participant_num'] = participant_num

        # RoomRetrieveSerializer 이용해
        serializer = self.serializer_class(instance=room)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = CustomJWTAuthentication.authenticate(self, request)
        room = self.get_object()
        room_leader = room.leader.pk

        # 채팅방 leader 와 로그인 유저가 다르면 오류 메세지 출력
        if user != room_leader:
            return JsonResponse(
                {"error_message": "This user is not room host"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

# class CategoryListView(ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryListSerializer


class ChatUserView(ListCreateAPIView, DestroyAPIView):
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer

    def get(self, reqeust, room_id):
        user_list = ChatUser.objects.filter(room_id=room_id)
        print("user_list", user_list)
        serializer = ChatUserSerializer(instance=user_list, many=True)

        return Response({"users": serializer.data})

    def post(self, request, room_id):
        # path-variable <int:room_id>로 받아온 채팅방 인덱스 통해 Room 객체 get
        try:
            room = Room.objects.get(id=room_id)
            # 로그인 유저 pk
            user_pk = CustomJWTAuthentication.authenticate(self, request)

            # serializer 없이 직접 생성
            ChatUser.objects.create(
                room=room,
                user=User.objects.get(id=user_pk)
            )

            return Response(status=status.HTTP_201_CREATED)
        except Room.DoesNotExist:
            return Response({"message": "room does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, room_id):
        user_pk = CustomJWTAuthentication.authenticate(self, request)

        try:
            chat_user = ChatUser.objects.get(room_id=room_id, user_id=user_pk)
            chat_user.delete()
            return Response(status=status.HTTP_200_OK)

        except ChatUser.DoesNotExist:
            return Response({"message": "user not included in this room"}, status=status.HTTP_400_BAD_REQUEST)


class CurrentLocationView(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = CurLocationSerializer

    def post(self, request):
        room_id = request.data['room_id']
        user_id = CustomJWTAuthentication.authenticate(self, request)

        cur_latitude = request.data['cur_latitude']
        cur_longitude = request.data['cur_longitude']

        try:
            chat_user = ChatUser.objects.get(room_id=room_id, user_id=user_id)

            try:
                cur_location_obj = Location.objects.get(room_id=room_id, user_id=user_id)
                # 전달 받은 채팅방 객체와 유저 객체 값을 갖는 Location 객체가 있으면
                # 현재 위도,경도 값에 새롭게 요청 받은 위도,경도 값을 할당한 후 save()
                cur_location_obj.cur_latitude = cur_latitude
                cur_location_obj.cur_longitude = cur_longitude
                cur_location_obj.save()
                return Response({"message": "current_location_updated"}, status=status.HTTP_200_OK)

            except Location.DoesNotExist:

                Location.objects.create(
                    room=Room.objects.get(id=room_id),
                    user=User.objects.get(id=user_id),
                    cur_latitude=cur_latitude,
                    cur_longitude=cur_longitude
                )
                return Response({"message": "current_location_created"}, status=status.HTTP_201_CREATED)

        except ChatUser.DoesNotExist:
            return Response({"message": "user not included in this room"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        room_id = int(request.GET['room_id'])
        cur_location_list = Location.objects.filter(room_id=room_id)
        serializer = CurLocationSerializer(instance=cur_location_list, many=True)

        return Response({"location_list": serializer.data})
