from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone', 'paid', 'status', 'created_at']
    list_filter = ['status', 'paid', 'created_at']
    list_editable = ['status', 'paid']
    inlines = [OrderItemInline]
