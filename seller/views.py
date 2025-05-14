from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import ProductModel, OrderModel
from .forms import ProductForm
from django.db.models import Sum

# Create your views here.

@login_required
def seller_dashboard(request):
    user = request.user
    products = ProductModel.objects.filter(user=user)
    order = OrderModel.objects.filter(product__user=user)
    order_count = OrderModel.objects.filter(product__user=user, is_paid=True).count()
    product_count = products.count()
    total_earned = OrderModel.filter(is_paid=True).aggregate(total=Sum('total_price'))['total'] or 0

    context = {
        'user': user,
        'order': order,
        'order_count': order_count,
        'products': products,
        'product_count': product_count,
        'total_earned': total_earned,
    }
    return render(request, 'seller/dashboard.html', context)