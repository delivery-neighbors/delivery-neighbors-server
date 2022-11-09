from datetime import datetime
from collections import Counter

import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import ChatUser
from config.authentication import CustomJWTAuthentication
from neighbor.models import ChatUserReview, UserReliability
from neighbor.serializers import *

BASE_URL = "https://baedalius.com/"  # deploy version
# BASE_URL = "http://localhost:8000/"  # local version


class UserUpdateAPIView(generics.UpdateAPIView):
    def put(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        try:
            user = User.objects.get(id=user_id)

            username = request.POST['username']
            avatar = request.FILES.getlist('avatar')

            if user.is_active:
                user.username = username
                if avatar:
                    user.avatar = avatar[0]
                else:
                    user.avatar = 'media/avatar/default_img.jpg'

                serializer = UserUpdateSerializer(user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                return Response({"status": status.HTTP_200_OK, "data": serializer.data})

            else:
                return Response({"status": status.HTTP_400_BAD_REQUEST})

        except User.DoesNotExist:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, user_id):
        # 프로필 사진, 닉네임
        # 방장/참여자 참여 횟수, 신뢰도 점수
        # 해당 유저에게 리뷰 남겼는지
        # top3 카테고리

        user = User.objects.get(id=user_id)

        reliability = UserReliability.objects.get(user=user)

        num_as_leader = reliability.num_as_leader
        num_as_participant = reliability.num_as_participant
        score = reliability.score

        # data = user.__dict__ & data['serializer_field_name'] = value 형태가 아닌
        # user.serializer_field_name = value 로도 값 지정 가능
        user.num_as_leader = num_as_leader
        user.num_as_participant = num_as_participant
        user.score = score

        categories = []
        for chat_user in ChatUser.objects.filter(user=user):
            categories.append(chat_user.room.category)

        # 유저가 참여한 모든 채팅방 카테고리가 들어있는
        # categories list 를 Counter 객체화
        category_counter = dict(Counter(categories))

        # 카운트 된 횟수로 내림차순 정렬 후 3개만 채택
        top3category = sorted(category_counter.items(), key=lambda x: x[1], reverse=True)[:3]

        top3_json = {}
        for i in range(len(top3category)):
            top3_json[i+1] = {"id": top3category[i][0].id, "category_name": top3category[i][0].category_name,
                              "category_img": str(top3category[i][0].category_background_img)}

        user.top3category = top3_json.values()

        serializer = UserSerializer(instance=user)

        return Response({"status": status.HTTP_200_OK, "user": serializer.data})


class UserMyPageAPIView(RetrieveAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)
        user = User.objects.get(id=user_id)
        avatar = user.avatar
        reliability = UserReliability.objects.get(user=user)

        num_as_leader = reliability.num_as_leader
        num_as_participant = reliability.num_as_participant
        score = reliability.score

        data = user.__dict__
        data['num_as_leader'] = num_as_leader
        data['num_as_participant'] = num_as_participant
        data['score'] = score

        serializer = MyPageSerializer(instance=data)

        return Response({"status": status.HTTP_200_OK, "data": serializer.data})


# ver 2)
class ReviewListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        reviewList = Review.objects.all()
        data = {
            'reviewList': reviewList,
        }
        serializer = ReviewSerializer(instance=data)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})


class ReviewRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewRetrieveSerializer


class UserReviewListAPIView(generics.ListAPIView):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer

    def get(self, request, userid):
        user = User.objects.get(id=userid)

        review = UserReview.objects.filter(user_id=userid).order_by('-count')
        review_list = review[:3]
        serializer = UserReviewSerializer(review_list, many=True)

        return Response({"status": status.HTTP_200_OK, "data": serializer.data})


class UserReviewCreateView(generics.CreateAPIView):
    def post(self, request, chat_user_id):
        login_user_id = CustomJWTAuthentication.authenticate(self, request)
        login_user = User.objects.get(id=login_user_id)

        chat_user = ChatUser.objects.get(id=chat_user_id)
        room = chat_user.room
        user = chat_user.user

        review_index_list = request.data['review_list']

        if ChatUserReview.objects.filter(chat_user=chat_user, writer=login_user):
            return Response({"status": status.HTTP_208_ALREADY_REPORTED})

        else:
            for review_index in review_index_list:
                review = Review.objects.get(id=review_index)
                obj = UserReview.objects.get_or_create(user_id=user, review_id=review)
                obj[0].count += 1
                obj[0].save()

            ChatUserReview.objects.create(chat_user=chat_user, writer=login_user)

            review_count = len(ChatUserReview.objects.filter(writer=login_user, chat_user__room=room).
                               distinct().values_list('chat_user'))

            if review_count == room.max_participant_num - 1:
                chat_user_obj = ChatUser.objects.get(user=login_user, room=room)
                chat_user_obj.review_status = True
                chat_user_obj.save()

            reliability = UserReliability.objects.get(user=user)
            if 1 <= review_index <= 6:
                reliability.score += 2
                reliability.save()
            else:
                reliability.score -= 2
                reliability.save()

            return Response({"status": status.HTTP_200_OK})


class UserAddressView(ListCreateAPIView, DestroyAPIView):
    def post(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        addr_latitude = request.data['addr_latitude']
        addr_longitude = request.data['addr_longitude']

        try:
            address = Address.objects.get(user_id=user_id, addr_latitude=addr_latitude, addr_longitude=addr_longitude)

            # 이미 등록된 주소면 updated_at 최신화
            updated_at = address.updated_at
            print("update time", updated_at)

            address.save()

            return Response({"status": status.HTTP_200_OK})

        except Address.DoesNotExist:
            addr = Address.objects.create(
                user=User.objects.get(id=user_id),
                addr_latitude=addr_latitude,
                addr_longitude=addr_longitude
            )

            return Response({"status": status.HTTP_201_CREATED})

    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        addr_list = Address.objects.filter(user_id=user_id).order_by('-updated_at')
        print("addr_list", addr_list.values())

        if len(addr_list) >= 3:
            addr_list = addr_list[:3]

        serializer = UserAddressSerializer(instance=addr_list, many=True)

        return Response({"status": status.HTTP_200_OK, "addr_list": serializer.data})


class UserAddressDestroyView(DestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args)
        instance.delete()
        return Response({"status": status.HTTP_204_NO_CONTENT})


# kakao map
def kakao_map(request):
    return render(request, 'LoadNameAddress.php')


class UserRecentSearchView(ListAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        search_list = Search.objects.filter(user=user_id).order_by('-created_at')[:10]
        serializer = UserSearchSerializer(instance=search_list, many=True)

        return Response({"status": status.HTTP_200_OK, "search_list": serializer.data})


class UserSearchDestroyAPIView(DestroyAPIView):
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        return Search.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args)
        instance.delete()
        return Response({"status": status.HTTP_204_NO_CONTENT})


@csrf_exempt
def Top10_SearchedAPIView(request):
    files_path = "./media/images/wordcloud/"
    file_name_and_time_lst = []

    file_list = os.listdir(files_path)
    for f_name in file_list:
        written_time = os.path.getctime(f"{files_path}{f_name}")
        file_name_and_time_lst.append((f_name, written_time))
    sorted_file_lst = sorted(file_name_and_time_lst, key=lambda x: x[1], reverse=True)
    recent_file = sorted_file_lst[0]
    recent_file_name = recent_file[0]
    return JsonResponse({"status": status.HTTP_200_OK, "wordcloud_url": f"{BASE_URL}media/images/wordcloud/{recent_file_name}"})


def toss_view(request):
    return render(request, 'tosspayments.html')


class UserIdCheckAPIView(RetrieveAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)
        user = User.objects.get(id=user_id)
        serializer = UserIdCheckSerializer(instance=user)
        return Response({"status": status.HTTP_200_OK, "data": serializer.data})

