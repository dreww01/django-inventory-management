from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import ProductForm


# Home / dashboard view – per user
@login_required
def home_view(request):
    user_products = Product.objects.filter(owner=request.user)

    total_products = user_products.count()
    low_stock = user_products.filter(quantity__lte=10).count()
    out_of_stock = user_products.filter(quantity=0).count()
    latest_products = user_products.order_by('-Product_id')[:8]

    context = {
        'total_products': total_products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'latest_products': latest_products,
    }
    return render(request, 'invApp/home.html', context)


# Create view – creates a product for the logged-in user
@login_required
def product_create_view(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)   # do not save yet
            product.owner = request.user        # attach owner
            product.save()                      # now save
            messages.success(request, 'Product created!')
            return redirect('product_list_view')

    return render(request, 'invApp/product_form.html', {'form': form})


# List view – only this user's products
@login_required
def product_list_view(request):
    products = Product.objects.filter(owner=request.user)
    return render(request, 'invApp/product_list.html', {'products': products})


# Update view – only allow editing products owned by this user
@login_required
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated!')
            return redirect('product_list_view')
    else:
        form = ProductForm(instance=product)

    return render(request, 'invApp/product_form.html', {'form': form})


# Delete view – only allow deleting products owned by this user
@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted!')
        return redirect('product_list_view')

    return render(request, 'invApp/product_confirm_delete.html', {'product': product})
