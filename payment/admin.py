from django.contrib import admin

from payment.models import Pay


class PayAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'amount']


admin.site.register(Pay, PayAdmin)
