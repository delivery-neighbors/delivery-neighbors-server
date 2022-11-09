from django.db import models

from accounts.models import User


class Review(models.Model):
    content = models.CharField(max_length=50)

    def __str__(self):
        return self.content


class UserReview(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.review_id} {self.count}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['review_id', 'user_id'],
                name="user-review"
            )
        ]


class ChatUserReview(models.Model):
    chat_user = models.ForeignKey('chat.ChatUser', on_delete=models.CASCADE)
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)


class Address(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    addr_latitude = models.DecimalField(max_digits=20, decimal_places=16)
    addr_longitude = models.DecimalField(max_digits=20, decimal_places=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_content = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserReliability(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    num_as_leader = models.IntegerField(default=0)
    num_as_participant = models.IntegerField(default=0)
    score = models.IntegerField(default=50)


class OrderFrequency(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category1 = models.IntegerField(default=0)
    category2 = models.IntegerField(default=0)
    category3 = models.IntegerField(default=0)
    category4 = models.IntegerField(default=0)
    category5 = models.IntegerField(default=0)
    category6 = models.IntegerField(default=0)
    category7 = models.IntegerField(default=0)
    category8 = models.IntegerField(default=0)
    category9 = models.IntegerField(default=0)
    category10 = models.IntegerField(default=0)
    category11 = models.IntegerField(default=0)
    category12 = models.IntegerField(default=0)
    total = models.IntegerField(default=0)


class Report(models.Model):
    reporter_id = models.IntegerField()
    reported_id = models.IntegerField()
    content = models.CharField(max_length=500)
