from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from chat.models import ChatUser
from config.authentication import CustomJWTAuthentication
from neighbor.models import Review, UserReview, Address, Search, ChatUserReview
from neighbor.serializers import ReviewSerializer, UserSerializer, UserReviewSerializer, ReviewRetrieveSerializer, \
    UserAddressSerializer, UserUpdateSerializer, UserSearchSerializer


class UserRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        try:
            user = User.objects.get(id=user_id)

            # TODO 빈 값 들어왔을 때 기본 이미지로 설정하기

            if user.is_active:
                user.username = request.data['username']
                user.avatar = request.data['avatar']

                serializer = UserUpdateSerializer(user, data=request.data, partial=False)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                return Response({"status": status.HTTP_200_OK, "data": {"user": serializer.data}})

            else:
                return Response({"status": status.HTTP_400_BAD_REQUEST})

        except User.DoesNotExist:
            return Response({"status": status.HTTP_400_BAD_REQUEST})


# ver 1)
# class ReviewListAPIView(generics.ListAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer


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
        review = UserReview.objects.filter(user_id=userid)
        serializer = UserReviewSerializer(review, many=True)

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

            return Response({"status": status.HTTP_200_OK})


# @api_view(('GET',))
# def user_review_update(request, userid, reviewid):
#     print(userid, reviewid)
#     try:
#         user = User.objects.get(id=userid)
#         review = Review.objects.get(id=reviewid)
#         obj = UserReview.objects.get_or_create(user_id=user, review_id=review)
#         obj[0].count += 1
#         obj[0].save()
#         serializer = UserReviewSerializer(obj[0])
#         print(obj[0])
#         return Response({"status": status.HTTP_200_OK, "data": serializer.data})
#
#     except Review.DoesNotExist:
#         return Response({"status": status.HTTP_204_NO_CONTENT})


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
