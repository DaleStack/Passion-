from django.contrib import admin
from .models import ProductModel, CategoryModel, OrderModel
# Register your models here.

admin.site.register(ProductModel)
admin.site.register(CategoryModel)
@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price',)
    fields = ('product', 'buyer', 'quantity', 'is_paid', 'total_price')
    list_display = ['product', 'total_price', 'quantity']
