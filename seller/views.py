from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import ProductModel, OrderModel, CategoryModel
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
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '')

    products = ProductModel.objects.filter(user=user).order_by('-id')
    orders = OrderModel.objects.filter(product__in=products).order_by('-ordered_at')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if status_filter == 'in':
        products = products.filter(stock__gt=25)
    elif status_filter == 'low':
        products = products.filter(stock__gte=15, stock__lte=25)
    elif status_filter == 'limited':
        products = products.filter(stock__gte=1, stock__lt=15)
    elif status_filter == 'out':
        products = products.filter(stock=0)

    context = {
        'products': products,
        'orders': orders
    }
    return render(request, 'seller/partials/products.html', context)


@login_required
def add_product(request):
    user = request.user

    if user.role != 'Seller':
        messages.error(request, 'You are not authorized to view this page')
        return redirect('buyer_dashboard')
    
    categories = CategoryModel.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = user
            product.save()
            messages.success(request, 'New Product Added!')

            return redirect('seller:seller_dashboard')  # Or wherever appropriate
    else:
        form = ProductForm()

    return render(request, 'seller/add_product.html', {
        'form': form,
        'categories': categories,
    })

@login_required
def delete_product(request, pk):
    user = request.user

    if user.role != 'Seller':
        messages.error(request, 'You are not authorized to view this page')
        return redirect('buyer_dashboard')
    
    product = get_object_or_404(ProductModel, pk=pk)

    if product.user != user:
        messages.error(request, 'You can only delete your own products.')
        return redirect('seller:seller_dashboard')

    if request.method == "POST":
        orders = OrderModel.objects.filter(product=product)

        for order in orders:
            order.product = None  # Unlink product but keep order data
            order.save()

        product.delete()

        messages.success(request, 'Product deleted!')
        return redirect('seller:seller_dashboard')


@login_required
def analytics_view(request):
    return render(request, 'seller/partials/analytics.html')

@login_required
def settings_view(request):
    return render(request, 'seller/partials/settings.html')