from django.urls import path
from .views import seller_dashboard

urlpatterns = [
    path('dashboard/', seller_dashboard, name='seller_dashboard'),
]
