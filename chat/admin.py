from django.contrib import admin
from chat.models import Category, Room, ChatUser, Location


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'leader', 'room_name', 'created_at', 'is_active']


class ChatUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'date_joined']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(Location, LocationAdmin)

