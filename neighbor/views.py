from rest_framework import generics
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
        return Response(serializer.data)


class ReviewRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewRetrieveSerializer


class UserReviewListAPIView(generics.ListAPIView):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer

    def get(self, request, userid):
        review = UserReview.objects.filter(user_id=userid)
        serializer = UserReviewSerializer(review, many=True)

        return Response(serializer.data)


@api_view(('GET',))
def user_review_update(request, userid, reviewid):
    try:
        obj = UserReview.objects.get(user_id=userid, review_id=reviewid)
        obj.count += 1
        obj.save()
        serializer = UserReviewSerializer(obj)
        return Response(serializer.data)

    except UserReview.DoesNotExist:
        user_id = User.objects.get(id=userid)
        review_id = Review.objects.get(id=reviewid)
        obj = UserReview.objects.create(
            user_id=user_id,
            review_id=review_id
        )
        serializer = UserReviewSerializer(obj)
        return Response(serializer.data)
