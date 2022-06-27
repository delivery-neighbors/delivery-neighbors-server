from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from neighbor.models import Review, UserReview
from neighbor.serializers import ReviewSerializer, UserSerializer, UserReviewSerializer, ReviewRetrieveSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
    try:
        obj = UserReview.objects.get(user_id=userid, review_id=reviewid)
        obj.count += 1
        obj.save()
        serializer = UserReviewSerializer(obj)
        return Response({"status": status.HTTP_200_OK, "success": "true", "data": serializer.data})

    except UserReview.DoesNotExist:
        return Response({"status": status.HTTP_204_NO_CONTENT, "success": "false", "message": "this review is not exist"})
      

# kakao map
def kakao_map(request):
    return render(request, 'LoadNameAddress.php')
  