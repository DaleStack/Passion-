from django.urls import path
from .views import test

urlpatterns = [
    path('test/', test, name='seller_dashboard')
]
