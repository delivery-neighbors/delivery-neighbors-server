from django.contrib import admin
from chat.models import Category, Room, ChatUser, Location


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'leader', 'room_name', 'created_at', 'status']


class ChatUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'date_joined']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'cur_latitude', 'cur_longitude']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(Location, LocationAdmin)

