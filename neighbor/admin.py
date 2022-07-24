from django.contrib import admin

from accounts.models import User
from neighbor.models import Review, UserReview, Address, Search, ChatUserReview, UserReliability


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
    list_display = ['id', 'user', 'addr_latitude', 'addr_longitude', 'created_at', 'updated_at']


class SearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'search_content', 'created_at', 'updated_at']


class ChatUserReviewAdmin(admin.ModelAdmin):
    list_display = ['chat_user', 'writer']


class UserReliabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'num_as_leader', 'num_as_participant', 'score']


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(ChatUserReview, ChatUserReviewAdmin)
admin.site.register(UserReliability, UserReliabilityAdmin)

