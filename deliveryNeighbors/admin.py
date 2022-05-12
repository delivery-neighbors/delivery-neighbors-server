from django.contrib import admin

from deliveryNeighbors.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'email', 'created_at']


admin.site.register(User, UserAdmin)
