from django.urls import path
from .views import buyer_dashboard

app_name = 'buyer'

urlpatterns = [
    path('buyer-dashboard/', buyer_dashboard, name="buyer_dashboard"),
]
