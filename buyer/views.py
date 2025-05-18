from django.shortcuts import render, redirect, get_object_or_404
from seller.models import ProductModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
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

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.quantity > product.stock:
                messages.error(request, f"Only {product.stock} items in stock.")
                return redirect('buyer:item_view', pk=pk)

            order.product = product
            order.buyer = request.user
            order.is_paid = True  # Mark as paid
            order.save()

            # Reduce product stock
            product.stock -= order.quantity
            product.save()

            messages.success(request, "Item added to your orders!")
            return redirect('buyer:buyer_dashboard')
    else:
        form = OrderForm()

    return render(request, 'buyer/item_view.html', {
        'product': product,
        'form': form,
    })


