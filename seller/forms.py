from django import forms
from .models import ProductModel

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['category', 'name', 'image', 'description', 'price', 'stock', ]