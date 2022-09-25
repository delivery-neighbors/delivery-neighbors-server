from datetime import timedelta

from rest_framework import status
from rest_framework.response import Response

import pandas
from django.utils.datetime_safe import datetime
from haversine import haversine, Unit
from sklearn.metrics.pairwise import cosine_similarity

from rest_framework.generics import *

from accounts.models import User
from chat.models import Room, ChatUser
from config.authentication import CustomJWTAuthentication
from neighbor.models import OrderFrequency, Address
from recommendation.serializers import SimilarUserChatroomSerializer


class SimilarUserListView(ListAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        # data = pandas.read_csv('file/user_order_data.csv')
        #
        # order_frequency = (data['orderFrequency'] / data['total']).to_frame()
        # order_frequency.columns = ['order']
        #
        # data = pandas.merge(data, order_frequency, left_index=True, right_index=True)
        #
        # pivot_data = data.pivot(index='userId', columns='categoryId', values='order')
        #
        # user_similarity = cosine_similarity(pivot_data)
        # # print("user_similarity\n", user_similarity)
        #
        # user_similarity_df = pandas.DataFrame(data=user_similarity, index=pivot_data.index, columns=pivot_data.index)
        #
        # print('-------------------------------------------------------------------------------')
        # cosine_sim_top5_list = user_similarity_df[user_id].sort_values(ascending=False)[1:4]
        # print("코사인 유사도 상위 3위", cosine_sim_top5_list.index, "\n", cosine_sim_top5_list)

        cosine_sim_top5_list = [3, 5, 7]

        address = Address.objects.filter(user=user_id).order_by('-created_at')
        request_latitude = address[0].addr_latitude
        request_longitude = address[0].addr_longitude
        request_location = (request_latitude, request_longitude)

        rec_rooms = []

        # 비슷한 유저가 가장 최근에 만든 채팅방 or
        # 만든 게 없으면 가장 최근에 참여한 채팅방으로 3개 내보내기

        for userId in cosine_sim_top5_list:
            user = User.objects.get(id=userId)

            room = list(Room.objects.filter(leader=user))

            if room:
                rec_rooms.append(room[-1])

            else:
                last_joined_room = ChatUser.objects.filter(user=user)

                if not last_joined_room:
                    continue

                last_joined_room = list(last_joined_room)
                room = Room.objects.get(id=last_joined_room[-1])
                rec_rooms.append(room)

        for room in rec_rooms:
            room_id = room.id

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
            participant_num = ChatUser.objects.filter(room_id=room_id).count()

            room = room.__dict__
            room['distance'] = int(distance)
            room['participant_num'] = participant_num

        serializer = SimilarUserChatroomSerializer(instance=rec_rooms, many=True)
        return Response({"status": status.HTTP_200_OK, "rooms": serializer.data})
