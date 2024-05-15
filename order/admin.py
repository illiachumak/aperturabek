from django.contrib import admin
from .models import Order, OrderProduct, Feedback

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name','order_number', 'email', 'status', 'total_price', 'payment')
    search_fields = ['name', 'email', 'order_number']

class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('name','number', 'is_Called')
    search_fields = ['name', 'number']


admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedBackAdmin)