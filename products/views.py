from http.client import HTTPResponse
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from category.models import Category 
from products.models import Product 
from django.http import HttpResponse
from django.db.models import Q
from extra.models import Productoffer, Categoryoffer

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.


def store (request,category_slug=None):
    category = None 
    products = None
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category, is_available = True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
        for r in products:
            try:
                Coffer = Categoryoffer.objects.get(category = r.category)
                Cat    = Coffer.discount
                if Coffer:
                    r.discount = int(r.price - (r.price*(Cat/100)))
                    r.save()
            except:
                r.discount = None
                r.save()
    else: 
        products = Product.objects.all().filter(is_available = True)
        for r in products:
            try:
                Poffer = Productoffer.objects.get(product = r.id)
                Prod   = Poffer.discount
                if Poffer:
                    r.discount = int(r.price - (r.price*(Prod/100)))
                    r.save()
            except:
                r.discount = None
                r.save()
        paginator = Paginator(products,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    context = {
        'products': paged_products,
        'products_count' : products_count,
    }
    
    return render (request,'productuser.html',context)

# def product_detail(request , category_slug, product_slug):
#     try:
#         single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
#     except Exception as e
#     raise e 

#     context = {
#         'single_product': single_product,
#     }
#     return render(request,'product-detail.html', context)


        #in_cart = Cartitem.objects.filter(cart_cart_id = _cart_id(request),product = single_product).exists()


def product_detail(request, id):
    product=Product.objects.get(id=id)
    return render(request,'product-detail.html',{'product':product})


def demo (request):
    return render(request,'hello.html')


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count,
    }
    return render (request,'productuser.html', context)

