from rest_framework import generics
from rest_framework.decorators import api_view
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


@api_view(('GET',))
def user_review_update(request, userid, reviewid):
    try:
        obj = UserReview.objects.get(user_id=userid, review_id=reviewid)
        obj.count += 1
        obj.save()
        serializer = UserReviewSerializer(obj)
        return Response(serializer.data)

    except UserReview.DoesNotExist:
        user_id = User.objects.get_object_or_404(id=userid)  # 유저나 리뷰 없으면 404 에러
        review_id = Review.objects.get_object_or_404(id=reviewid)
        obj = UserReview.objects.create(
            user_id=user_id,
            review_id=review_id
        )
        serializer = UserReviewSerializer(obj)
        return Response(serializer.data)
