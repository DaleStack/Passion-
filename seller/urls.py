from django.urls import path
from .views import seller_dashboard, products_view, analytics_view, settings_view, add_product, delete_product, edit_product

app_name = 'seller'

urlpatterns = [
    path('dashboard/', seller_dashboard, name='seller_dashboard'),
    path('products/', products_view, name='products'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:pk>/', edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', delete_product, name='delete_product'),
    path('analytics/', analytics_view, name='analytics'),
    path('settings/', settings_view, name='settings'),
]
