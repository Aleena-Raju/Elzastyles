from urllib import request
from django .shortcuts import render,redirect
from products.models import Product





def home(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products' : products
    }
    return render(request,'index.html', context)