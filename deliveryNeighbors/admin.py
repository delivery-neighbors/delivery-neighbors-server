from django.contrib import admin

from deliveryNeighbors.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'date_joined']


admin.site.register(User, UserAdmin)
