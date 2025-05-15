from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import ProductModel, OrderModel
from .forms import ProductForm
from django.db.models import Sum
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

@login_required
def seller_dashboard(request):
    user = request.user
    
    if user.role != 'Seller':
        messages.error(request, 'You are not authorized to view this page')
        return redirect('buyer_dashboard')
    
    products = ProductModel.objects.filter(user=user)
    orders = OrderModel.objects.filter(product__user=user)
    order_count = OrderModel.objects.filter(product__user=user, is_paid=True).count()
    product_count = products.count()
    total_earned = orders.filter(is_paid=True).aggregate(total=Sum('total_price'))['total'] or 0

    context = {
        'user': user,
        'orders': orders,
        'order_count': order_count,
        'products': products,
        'product_count': product_count,
        'total_earned': total_earned,
    }
    return render(request, 'seller/dashboard.html', context)

@login_required
def products_view(request):
    user = request.user
    products = ProductModel.objects.filter(user=user)

    context = {
        'products': products,
    }
    return render(request, 'seller/partials/products.html', context)

@login_required
def orders_view(request):
    return render(request, 'seller/partials/orders.html')

@login_required
def analytics_view(request):
    return render(request, 'seller/partials/analytics.html')

@login_required
def settings_view(request):
    return render(request, 'seller/partials/settings.html')