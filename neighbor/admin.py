from django.contrib import admin

from accounts.models import User
from neighbor.models import Review, UserReview, Address


class UserReviewInline(admin.TabularInline):
    model = UserReview
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (UserReviewInline,)
    list_display = ['id', 'email', 'username', 'date_joined']
    list_display_links = ['id', 'email']  # 링크로 표시할 필드


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'review_id', 'count']
    list_filter = ['user_id']  # 필터 처리된 user_id를 우측에 보여줌
    ordering = ('-user_id', '-review_id', )


class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'addr_latitude', 'addr_longitude']


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(Address, AddressAdmin)
