from django import forms
from .models import ProductModel
from django.contrib.auth import get_user_model


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['category', 'name', 'image', 'description', 'price', 'stock', ]

UserModel = get_user_model()
class SettingForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email']
