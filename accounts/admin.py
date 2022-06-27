from django.contrib import admin
from .models import User, Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'addr_latitude', 'addr_longitude']


admin.site.register(Address, AddressAdmin)
