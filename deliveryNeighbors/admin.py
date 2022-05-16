from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'profile_img']
    fields = ['username', 'email', 'profile_img']


admin.site.register(User, UserAdmin)
