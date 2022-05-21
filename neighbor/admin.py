from django.contrib import admin

from neighbor.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']


admin.site.register(Review, ReviewAdmin)
