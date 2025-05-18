from django.shortcuts import render, redirect
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
