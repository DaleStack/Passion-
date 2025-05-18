from django.shortcuts import render, redirect, get_object_or_404
from seller.models import ProductModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
@login_required
def buyer_dashboard(request):
    user = request.user
    
    if user.role != 'Buyer':
        messages.error(request, 'You are not authorized to view this page')
        return redirect('seller:seller_dashboard')
    
    products = ProductModel.objects.all()

    context = {
        'user': user,
        'products': products,
    }
    return render(request, 'buyer/buyerdash.html', context)

@login_required
def item_view(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)

    return render(request, 'buyer/product_detail.html', {
        'product': product
    })



