from datetime import timedelta, datetime
from decimal import Decimal

from django.db.models import Q
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from chat.serializers import *
from config.authentication import CustomJWTAuthentication

from haversine import haversine, Unit

from neighbor.models import Address, Search


class RoomGetCreateAPIView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer

    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        category_id = int(request.GET['category_id'])

        # 채팅방 목록 조회 요청 시 user_latitude,user_longitude 입력 없이
        # 유저가 가장 최근에 입력한 주소로 get
        address = Address.objects.filter(user=user_id).order_by('-created_at')

        rooms_first_filtering = []

        if not address:
            return Response({"status": status.HTTP_204_NO_CONTENT, "rooms": rooms_first_filtering})

        else:
            request_latitude = address[0].addr_latitude
            request_longitude = address[0].addr_longitude
            request_location = (request_latitude, request_longitude)

            # filter()에 넣어줄 조건
            # 1km에 대해 위도는 0.01 차이, 경도는 0.015 차이
            # 즉, request 통해 받아온 위치(위도,경도)에서 +,- 0.005 (위도) / +,- 0.0075 (경도) 떨어진 곳까지 1차 필터링
            # Q 클래스 -> filter()에 넣어줄 논리 조건을 | 또는 & 사용해 조합 가능케 해줌
            condition = (
                    Q(pickup_latitude__range=(request_latitude - Decimal(0.005), request_latitude + Decimal(0.005))) &
                    Q(pickup_longitude__range=(
                    request_longitude - Decimal(0.0075), request_longitude + Decimal(0.0075)))
            )
            rooms_first_filtering = Room.objects.filter(condition)

            # 500m 이내 채팅방 2차 필터링
            rooms_within_500meters = [room for room in rooms_first_filtering
                                      if haversine(request_location,
                                                   (room.pickup_latitude, room.pickup_longitude),
                                                   unit=Unit.METERS) < 500]

            if category_id != 0:
                category = Category.objects.get(id=category_id)
                rooms_by_category = [room for room in rooms_within_500meters
                                     if room.category == category]
            else:
                rooms_by_category = rooms_within_500meters

            for room in rooms_by_category:
                room_id = room.id

                if user_id == room.leader.id:
                    is_leader = True

                else:
                    is_leader = False

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
                room['is_leader'] = is_leader
                room['distance'] = int(distance)
                room['participant_num'] = participant_num

            serializer = RoomListSerializer(instance=rooms_by_category, many=True)
            return Response({"status": status.HTTP_200_OK, "rooms": serializer.data})

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

        return Response({"status": status.HTTP_201_CREATED})


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
        return Response({"status": status.HTTP_200_OK, "room": serializer.data})

    def delete(self, request, *args, **kwargs):
        user = CustomJWTAuthentication.authenticate(self, request)
        room = self.get_object()
        room_leader = room.leader.pk

        if room.status != "JOINED":
            return Response({"status": status.HTTP_405_METHOD_NOT_ALLOWED})

        self.destroy(request, *args, **kwargs)
        return Response({"status": status.HTTP_200_OK})


class RoomGetByKeywordView(ListAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)
        user = User.objects.get(id=user_id)

        # 채팅방 목록 조회 요청 시 user_latitude,user_longitude 입력 없이
        # 유저가 가장 최근에 입력한 주소로 get
        address = Address.objects.filter(user=user_id).order_by('-created_at')

        request_search = request.GET['keyword']

        # 사용자의 주소 데이터가 없을 때
        if not address:
            return Response({"status": status.HTTP_400_BAD_REQUEST})

        # 키워드 없을 때
        if not request_search.strip():
            return Response({"status": status.HTTP_204_NO_CONTENT})

        search_instance = Search.objects.filter(user=user, search_content=request_search)

        # 검색어가 이미 존재하는 경우 기존의 검색어를 삭제하고 재생성
        if search_instance:
            search_instance.delete()

        Search.objects.create(user=user, search_content=request_search)

        request_latitude = address[0].addr_latitude
        request_longitude = address[0].addr_longitude
        request_location = (request_latitude, request_longitude)
        # filter()에 넣어줄 조건
        # 1km에 대해 위도는 0.01 차이, 경도는 0.015 차이
        # 즉, request 통해 받아온 위치(위도,경도)에서 +,- 0.005 (위도) / +,- 0.0075 (경도) 떨어진 곳까지 1차 필터링
        # Q 클래스 -> filter()에 넣어줄 논리 조건을 | 또는 & 사용해 조합 가능케 해줌
        condition = (
                Q(pickup_latitude__range=(request_latitude - Decimal(0.005), request_latitude + Decimal(0.005))) &
                Q(pickup_longitude__range=(request_longitude - Decimal(0.0075), request_longitude + Decimal(0.0075))) &
                Q(room_name__contains=request_search)
        )
        rooms_first_filtering = Room.objects.filter(condition)

        # 500m 이내 채팅방 2차 필터링
        rooms_within_500meters = [room for room in rooms_first_filtering
                                  if haversine(request_location,
                                               (room.pickup_latitude, room.pickup_longitude),
                                               unit=Unit.METERS) < 500]

        for room in rooms_within_500meters:
            room_id = room.id

            if user_id == room.leader.id:
                is_leader = True

            else:
                is_leader = False

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
            room['is_leader'] = is_leader
            room['distance'] = int(distance)
            room['participant_num'] = participant_num

        serializer = RoomListSerializer(instance=rooms_within_500meters, many=True)
        return Response({"status": status.HTTP_200_OK, "rooms": serializer.data})


# class CategoryListView(ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryListSerializer


class ChatUserView(ListCreateAPIView, DestroyAPIView):
    queryset = ChatUser.objects.all()

    def get(self, reqeust, room_id):
        user_list = ChatUser.objects.filter(room_id=room_id)
        serializer = ChatUserSerializer(instance=user_list, many=True)

        return Response({"status": status.HTTP_200_OK, "users": serializer.data})

    def post(self, request, room_id):
        # path-variable <int:room_id>로 받아온 채팅방 인덱스 통해 Room 객체 get
        room = Room.objects.get(id=room_id)
        # 로그인 유저 pk
        user_pk = CustomJWTAuthentication.authenticate(self, request)

        try:
            chat_user = ChatUser.objects.get(user_id=user_pk, room_id=room_id)
            return Response({"status": status.HTTP_200_OK})

        except ChatUser.DoesNotExist:
            # serializer 없이 직접 생성
            if len(ChatUser.objects.filter(room=room, status="JOINED")) >= room.max_participant_num:
                return Response({"status": status.HTTP_403_FORBIDDEN})

            ChatUser.objects.create(
                room=room,
                user=User.objects.get(id=user_pk)
            )

        return Response({"status": status.HTTP_201_CREATED})

    def delete(self, request, room_id):
        user_pk = CustomJWTAuthentication.authenticate(self, request)
        room = Room.objects.get(id=room_id)

        try:
            chat_user = ChatUser.objects.get(room_id=room_id, user_id=user_pk)

            if room.status != "JOINED":  # Room.status 가 JOINED 가 아닌 상황(주문확정, 결제완료, 수령완료)에는 채팅방 나가기 불가
                return Response({"status": status.HTTP_405_METHOD_NOT_ALLOWED})

            else:
                chat_user.delete()
                return Response({"status": status.HTTP_200_OK})

        except ChatUser.DoesNotExist:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


class ChatListDeleteView(RetrieveAPIView):
    def get(self, request, room_id):
        user_id = CustomJWTAuthentication.authenticate(self, request)
        room = Room.objects.get(id=room_id)

        try:
            if room.status != "DONE":  # Room.status 가 DONE 이 아니면 목록에서 지우기 불가
                return Response({"status": status.HTTP_405_METHOD_NOT_ALLOWED})

            chat_user_obj = ChatUser.objects.get(room_id=room_id, user_id=user_id)
            chat_user_obj.status = "DELETED"
            chat_user_obj.save()
            return Response({"status": status.HTTP_200_OK})

        except ChatUser.DoesNotExist:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


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
                return Response({"status": status.HTTP_200_OK})

            except Location.DoesNotExist:

                Location.objects.create(
                    room=Room.objects.get(id=room_id),
                    user=User.objects.get(id=user_id),
                    cur_latitude=cur_latitude,
                    cur_longitude=cur_longitude
                )
                return Response({"status": status.HTTP_201_CREATED})

        except ChatUser.DoesNotExist:
            return Response({"status": status.HTTP_400_BAD_REQUEST})

    def get(self, request):
        room_id = int(request.GET['room_id'])
        cur_location_list = Location.objects.filter(room_id=room_id)
        serializer = CurLocationSerializer(instance=cur_location_list, many=True)

        return Response({"status": status.HTTP_200_OK, "location_list": serializer.data})


class ChatJoinedView(ListAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        chat_user = ChatUser.objects.filter(user_id=user_id)
        print("chat_user", chat_user)

        address = Address.objects.filter(user=user_id).order_by('-created_at')
        request_latitude = address[0].addr_latitude
        request_longitude = address[0].addr_longitude
        request_location = (request_latitude, request_longitude)

        joined_room = []

        for i in chat_user:
            room = Room.objects.get(id=i.room_id)
            if room.status != "DONE":
                joined_room.append(room)

        for room in joined_room:
            room_id = room.id

            if user_id == room.leader.id:
                is_leader = True

            else:
                is_leader = False

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
            room['is_leader'] = is_leader
            room['distance'] = int(distance)
            room['participant_num'] = participant_num

        serializer = RoomListSerializer(instance=joined_room, many=True)
        return Response({"status": status.HTTP_200_OK, "joined_room": serializer.data})


class ChatDoneListView(ListAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        room_idx = ChatUser.objects.filter(user_id=user_id).exclude(status="DELETED")

        joined_room = []

        for i in room_idx:
            room = Room.objects.get(id=i.room_id)
            if room.status == "DONE":
                joined_room.append(room)

        for room in joined_room:
            room_id = room.id

            if user_id == room.leader.id:
                is_leader = True

            else:
                is_leader = False

            # 현재 채팅방 참여자 수 추출
            participant_num = ChatUser.objects.filter(room_id=room_id).count()

            # 로그인 유저 해당 채팅방 리뷰 작성 완료 여부 추출
            review_status = ChatUser.objects.get(room_id=room_id, user_id=user_id).review_status
            print("review status", review_status)

            # 거리, 현재 채팅방 참여자 수 정보 추가를 위해 room 객체를 dict 로 변환 뒤
            # 해당 dict 에 participant_num key-value 추가
            room = room.__dict__
            room['is_leader'] = is_leader
            room['participant_num'] = participant_num
            room['review_status'] = review_status

        serializer = RoomDoneSerializer(instance=joined_room, many=True)

        return Response({"status": status.HTTP_200_OK, "joined_room": serializer.data})


class ChatDoneView(RetrieveAPIView):
    queryset = ChatUser.objects.all()

    # 방 번호 전달 받아 user_id, room_id 로 ChatUser 객체 조회 후 상태(status) 변경
    def get(self, request, room_id):
        user_id = CustomJWTAuthentication.authenticate(self, request)
        chat_user_list = ChatUser.objects.filter(room_id=room_id)

        try:
            chat_user = chat_user_list.get(user_id=user_id)

            chat_user.status = "DONE"
            chat_user.save()

            for chat_user in chat_user_list:
                if chat_user.status != "DONE":
                    return Response({"status": status.HTTP_200_OK})

            room = Room.objects.get(id=room_id)
            room.status = "DONE"
            room.save()

            return Response({"status": status.HTTP_200_OK})

        except ChatUser.DoesNotExist:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


class RoomWithUserStatusListView(ListAPIView):
    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        room_status = room.status
        leader = room.leader

        status_dict = {"JOINED": "주문 확정 중", "CONFIRMED": "결제 중", "PAY_DONE": "수령 중", "DONE": "수령 완료"}
        status_list = list(status_dict.keys())
        status_value = status_dict.get(room_status, "수령 완료")
        idx = status_list.index(room_status)  # status 의 인덱스 값

        joined_user = ChatUser.objects.filter(room=pk).exclude(user=leader)
        for chat_user in joined_user:
            status_proceeding = False
            if chat_user.status == 'DONE':  # '수령 완료' 이면 모든 유저 status 가 True
                status_proceeding = True
            elif chat_user.status == status_list[idx + 1] or chat_user.status == 'DELETED':  # DELETED -> 이미 방이 DONE이 되었다는 뜻이므로 무조건 TRUE 출력
                status_proceeding = True
            chat_user = chat_user.__dict__
            chat_user['status'] = status_proceeding

        serializer = ChatUserStatusSerializer(instance= joined_user, many=True)
        return Response({"status": status.HTTP_200_OK, "room_status": status_value, "user_status": serializer.data})


class MyInfoByRoomAPIView(ListAPIView):
    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        user_id = CustomJWTAuthentication.authenticate(self, request)
        chat_user = ChatUser.objects.get(room=room, user=user_id)

        my_data = {
            "id": chat_user.id,
            "is_leader": True if user_id==room.leader.id else False,
            "status": chat_user.status
        }

        serializer = MyInfoByRoomSerializer(room)
        return Response({"status": status.HTTP_200_OK, "room": serializer.data, "user": my_data})