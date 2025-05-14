from django.contrib import admin
from .models import ProductModel, CategoryModel, OrderModel
# Register your models here.

admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(OrderModel)
