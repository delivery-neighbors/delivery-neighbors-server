from django.contrib import admin
from chat.models import Category, Room, ChatUser


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Room)
admin.site.register(ChatUser)
