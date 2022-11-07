from datetime import timedelta

from rest_framework import status
from rest_framework.response import Response

import pandas
from django.utils.datetime_safe import datetime
from haversine import haversine, Unit
from sklearn.metrics.pairwise import cosine_similarity

import numpy

from rest_framework.generics import *

from accounts.models import User
from chat.models import Room, ChatUser
from recommendation.models import  Recommended
from config.authentication import CustomJWTAuthentication
from neighbor.models import OrderFrequency, Address
from recommendation.serializers import SimilarUserChatroomSerializer


class SimilarUserListView(ListAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)
        login_user = User.objects.get(id=user_id)

        order_frequency_list = list(OrderFrequency.objects.all().values())

        row = len(order_frequency_list)
        col = 13

        user_category_matrix = numpy.full((row, col), 0.0)

        for i in range(0, len(order_frequency_list)):
            order_frequency = list(order_frequency_list[i].values())
            userId = order_frequency[1]
            total = order_frequency[14]

            for j in range(0, 12):
                user_category_matrix[i][0] = userId
                category_order = order_frequency[j + 2]
                if category_order == 0:
                    user_category_matrix[i][j + 1] = 0.0
                    continue
                frequency_res = category_order / total
                user_category_matrix[i][j + 1] = frequency_res

        # userId 열 데이터 타입 int 변경
        user_category_df = pandas.DataFrame(data=user_category_matrix,
                                            columns=['userId', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                                     '11', '12']).astype({'userId': 'int'})

        # userId 열 행 구분자로 바꾸기
        user_category_df.set_index(['userId'], inplace=True)
        print("유저 별 특정 카테고리 주문 빈도율\n", user_category_df)

        user_similarity = cosine_similarity(user_category_df)
        user_similarity_df = pandas.DataFrame(data=user_similarity,
                                              index=user_category_df.index, columns=user_category_df.index)

        cosine_sim_list = user_similarity_df[user_id].sort_values(ascending=False)[1:4].index
        print("코사인 유사도 계산 결과", cosine_sim_list, "\n")

        address = Address.objects.filter(user=user_id).order_by('-created_at')
        request_latitude = address[0].addr_latitude
        request_longitude = address[0].addr_longitude
        request_location = (request_latitude, request_longitude)

        rec_rooms = []

        # 비슷한 유저가 가장 최근에 만든 채팅방 or
        # 만든 게 없으면 가장 최근에 참여한 채팅방으로 3개 내보내기

        # 500m 이내 채팅방만,
        # 채팅방 상태가 JOINED인 경우만 필터링,
        # 자기가 만든 채팅방도 안 나오게 해야함 -> 유사도 결과값 1위는 본인이므로 유사도 리스트 0번은 제외한 유저의 채팅방을 가져옴

        for userId in cosine_sim_list:
            user = User.objects.get(id=userId)

            room = list(Room.objects.filter(leader=user).filter(status="JOINED"))

            if room:
                last_create = room[len(room)-1]
                rec_rooms.append(last_create)

            else:
                user_joined_chat = list(ChatUser.objects.filter(user=user))

                if not user_joined_chat:
                    continue

                joined_room = [chat.room for chat in user_joined_chat]
                last_joined_room = joined_room[len(joined_room)-1]

                if last_joined_room.status == "JOINED":
                    rec_rooms.append(last_joined_room)

        rec_rooms_within_500meters = [room for room in rec_rooms
                                      if haversine(request_location,
                                                   (room.pickup_latitude, room.pickup_longitude),
                                                   unit=Unit.METERS) < 500]

        for room in rec_rooms_within_500meters:
            now = datetime.now()
            created_at = room.created_at

            if now - created_at >= timedelta(days=365):
                room.created_at = created_at.strftime("%F")

            elif now - created_at >= timedelta(days=1):
                room.created_at = created_at.strftime("%m.%d")

            elif now - created_at >= timedelta(hours=1):
                created_at = int((now - created_at).seconds / 3600)
                room.created_at = str(created_at) + "시간 전"

            elif now - created_at > timedelta(minutes=1):
                created_at = int((now - created_at).seconds / 60)
                room.created_at = str(created_at) + "분 전"

            else:
                room.created_at = "방금 전"

            # 1인당 배달비 계산
            delivery_fee = room.delivery_fee
            max_participant_num = room.max_participant_num
            del_fee_for_person = int(delivery_fee / max_participant_num)
            room.delivery_fee = del_fee_for_person

            # 거리 계산
            distance = haversine(request_location, (room.pickup_latitude, room.pickup_longitude), unit=Unit.METERS)

            # 현재 채팅방 참여자 수
            participant_num = ChatUser.objects.filter(room=room).count()

            room = room.__dict__
            room['distance'] = int(distance)
            room['participant_num'] = participant_num

        # 추천 채팅방 조회 시 생성된 추천 이웃 3명 저장(바뀌면 업데이트)
        recommended = Recommended.objects.get_or_create(user=login_user,
                                                       rec_user1=cosine_sim_list[0],
                                                       rec_user2=cosine_sim_list[1],
                                                       rec_user3=cosine_sim_list[2])
        recommended[0].rec_user1 = cosine_sim_list[0]
        recommended[0].rec_user2 = cosine_sim_list[1]
        recommended[0].rec_user3 = cosine_sim_list[2]
        recommended[0].save()

        serializer = SimilarUserChatroomSerializer(instance=rec_rooms_within_500meters, many=True)
        return Response({"status": status.HTTP_200_OK, "rooms": serializer.data})
        # return Response({"status": status.HTTP_200_OK})

