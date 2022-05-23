from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=32)
    category_thumbnail = models.URLField(blank=True, null=True, max_length=512)
    category_background_img = models.URLField(blank=True, null=True, max_length=512)


class ChatUser(models.Model):
    # on_delete=models.CASCADE -> 참조되는 객체 삭제 시 참조하는 객체 함께 삭제
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)


class Room(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    leader = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=32)
    delivery_platform = models.CharField(max_length=10)
    delivery_fee = models.IntegerField()
    max_participant_num = models.IntegerField()
    pickup_address = models.TextField(null=True)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
