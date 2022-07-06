from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from config.authentication import CustomJWTAuthentication
from neighbor.models import Review, UserReview, Address, Search
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
        return Response({"status": status.HTTP_200_OK, "success": "true", "data": serializer.data})


class ReviewRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewRetrieveSerializer


class UserReviewListAPIView(generics.ListAPIView):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer

    def get(self, request, userid):
        review = UserReview.objects.filter(user_id=userid)
        serializer = UserReviewSerializer(review, many=True)

        return Response({"status": status.HTTP_200_OK, "success": "true", "data": serializer.data})


@api_view(('GET',))
def user_review_update(request, userid, reviewid):
    print(userid, reviewid)
    try:
        user = User.objects.get(id=userid)
        review = Review.objects.get(id=reviewid)
        obj = UserReview.objects.get_or_create(user_id=user, review_id=review)
        obj[0].count += 1
        obj[0].save()
        serializer = UserReviewSerializer(obj[0])
        print(obj[0])
        return Response({"status": status.HTTP_200_OK, "success": "true", "data": serializer.data})

    except Review.DoesNotExist:
        return Response({"status": status.HTTP_204_NO_CONTENT, "success": "false", "message": "this review is not exist"})


class UserAddressView(ListCreateAPIView, DestroyAPIView):
    def post(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        addr_latitude = request.data['addr_latitude']
        addr_longitude = request.data['addr_longitude']

        try:
            address = Address.objects.get(user_id=user_id, addr_latitude=addr_latitude, addr_longitude=addr_longitude)

            return Response({"status": status.HTTP_200_OK, "success": "true", "message": "already registered address"})

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

        return Response({"status": status.HTTP_200_OK, "success": "true", "addr_list": serializer.data})

    def delete(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        addr_latitude = request.data['addr_latitude']
        addr_longitude = request.data['addr_longitude']

        try:
            address = Address.objects.get(user_id=user_id, addr_latitude=addr_latitude, addr_longitude=addr_longitude)
            address.delete()
            return Response({"status": status.HTTP_200_OK, "success": "true"})

        except Address.DoesNotExist:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "success": "false", "message": "not registered address"})


# kakao map
def kakao_map(request):
    return render(request, 'LoadNameAddress.php')


class UserRecentSearchView(ListAPIView):
    def get(self, request):
        user_id = CustomJWTAuthentication.authenticate(self, request)

        search_list = Search.objects.filter(user=user_id).order_by('-created_at')
        if len(search_list) > 10:
            search_list = search_list[:10]
        serializer = UserSearchSerializer(instance=search_list, many=True)

        return Response({"status": status.HTTP_200_OK, "success": "true", "search_list": serializer.data})

