from django import forms
from seller.models import OrderModel

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['quantity']