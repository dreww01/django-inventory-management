from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm

# Create your views here.
# this is where we create CRUD logic -- CRUD -- create, read, update, delete

# home view
# def home_view(request):
#     return render(request, 'invApp/home.html')

def home_view(request):
    total_products = Product.objects.count()
    
    low_stock = Product.objects.filter(quantity__lte=10).count()      # less than or equal to 10 = low
    out_of_stock = Product.objects.filter(quantity=0).count()          # exactly 0

    latest_products = Product.objects.order_by('-Product_id')[:8]              # last 8 added

    context = {
        'total_products': total_products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'latest_products': latest_products,
    }
    return render(request, 'invApp/home.html', context)

# create view-- creates the product
def product_create_view(request):
    # instantiate your form from the roduct form
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        # check if the form data is valid
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created!')
            return redirect('product_list_view')
    context = {
        'form': form
    }
    return render(request, 'invApp/product_form.html', context)


# read view-- view all products
def product_list_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'invApp/product_list.html', context)


# update view
# we need to target the products by the product id-- pk
def product_update_view(request, pk):
    # get all products
    product = Product.objects.get(pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        # if form is written then update the product
        form = ProductForm(request.POST, instance=product)
        # check if the form data is valid, then save
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated!')
            return redirect('product_list_view')
    context = {
        'form': form
    }
    # if from is empty(!=POST), render the form
    return render(request, 'invApp/product_form.html', context)



# delete view-- pk=primary key
def product_delete_view(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted!')
        return redirect('product_list_view')
    return render(request, 'invApp/product_confirm_delete.html', {'product': product})
