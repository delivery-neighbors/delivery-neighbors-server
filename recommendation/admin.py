from django.contrib import admin

from recommendation.models import Recommended


class RecommendedAdmin(admin.ModelAdmin):
    list_display = ['user', 'rec_user1', 'rec_user2', 'rec_user3']


admin.site.register(Recommended, RecommendedAdmin)
