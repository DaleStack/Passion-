from django.urls import path
from .views import buyer_dashboard, item_view

app_name = 'buyer'

urlpatterns = [
    path('buyer-dashboard/', buyer_dashboard, name="buyer_dashboard"),
    path('item/<int:pk>/', item_view, name="item_view"),
]
