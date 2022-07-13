from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=32)
    category_background_img = models.ImageField(default='category/1.jpg', upload_to='images/category')


class ChatUser(models.Model):
    # on_delete=models.CASCADE -> 참조되는 객체 삭제 시 참조하는 객체 함께 삭제
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default="JOINED")  # JOINED/DELETED/DELIVERED
    review_status = models.BooleanField(default=False)


class Room(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    leader = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=32)
    delivery_platform = models.CharField(max_length=10)
    delivery_fee = models.IntegerField()
    max_participant_num = models.IntegerField()
    pickup_address = models.TextField(null=True)
    pickup_latitude = models.DecimalField(max_digits=20, decimal_places=16)
    pickup_longitude = models.DecimalField(max_digits=20, decimal_places=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Location(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    cur_latitude = models.DecimalField(max_digits=20, decimal_places=16)
    cur_longitude = models.DecimalField(max_digits=20, decimal_places=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 배달 수령 장소 도착 시 is_arrived 값을 True로 바꾸어줘
    # 바꾼 이후 다시 PUT 요청이 와도 업데이트 되지 않도록 함(수령 이후의 위치 정보 노출 방지 위함)
    is_arrived = models.BooleanField(default=False)
