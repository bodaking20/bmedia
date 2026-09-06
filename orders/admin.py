from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'service__category')
    search_fields = ('id', 'user__username', 'link', 'provider_order_id')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',) # يتيح لك تغيير حالة الطلب بسرعة من القائمة الخارجية