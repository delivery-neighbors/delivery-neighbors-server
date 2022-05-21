from django.db import models

from accounts.models import User


class Review(models.Model):
    content = models.CharField(max_length=50)

    def __str__(self):
        return self.content


class UserReview(models.Model):
    review_id = models.OneToOneField(Review, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return self.count

