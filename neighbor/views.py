from rest_framework import generics
from rest_framework.response import Response

from accounts.models import User
from neighbor.models import Review, UserReview
from neighbor.serializers import ReviewSerializer, UserSerializer, UserReviewSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class UserReviewListAPIView(generics.ListAPIView):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer

    def get(self, request, userid):
        review = UserReview.objects.filter(user_id=userid)
        serializer = UserReviewSerializer(review, many=True)

        return Response(serializer.data)
