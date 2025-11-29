from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta: # this describes the form attributes
        model = Product
        
        fields = ['name', 'sku', 'price', 'quantity', 'supplier']
        labels = {
            'product_id': 'Product ID',
            'name': 'Product Name',
            'sku': 'SKU',
            'price': 'Selling Price (₦)',
            'quantity': 'Quantity',
            'supplier': 'Product Supplier',
        }
        # widget used to style the form -- input attrributes
        widgets = {
            'product_id': forms.NumberInput(attrs={'placeholder': 'e.g. 124', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. socks', 'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'placeholder': 'e.g. SKU123', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'e.g. 200.40', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'e.g. 10', 'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'placeholder': 'e.g. Nike', 'class': 'form-control'}),
        } 
        