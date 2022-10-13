from django.shortcuts import render
from products.models import Product
from accounts.models import *
from cartapp.models import *
from django.contrib import messages
from category.models import *
from twilio.rest import Client
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import random
from .helper import MessageHandler
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from extra.models import *

# Create your views here.
def index(request):
    # values=Categoryies.objects.all()
    return render(request,'index.html')





#this function will save discount price in database 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    # -------------------- deactivate coupon after expiry date ------------------- #
    now=date.today()
    coupons=coupons.objects.filter(valid_to__lte=now)
    for y in coupons:
        y.active=False
        y.save()
    allproduct=Product.objects.all()
    allcategory=Category.objects.all()
    #looping through all products to calculate its discount Price
    for x in allproduct:
        list=[]
        # ------------------------ checking for category offer ----------------------- #
        try:
            category_offer=Categoryoffer.objects.get(category=x.category,is_active =True)
            list.append(category_offer.discount)
        except ObjectDoesNotExist:
            pass
        # ------------------------ checking for subcategory offer ----------------------- #
        # try:
        #     subcategory_offer=SubCategoryoffer.objects.get(subcategory=x.subcategories,is_active =True)
        #     list.append(subcategory_offer.discount)
        # except ObjectDoesNotExist:
        #     pass
        # ------------------------ checking for Product offer ----------------------- #
        try:
            product_offer=Productoffer.objects.get(product=x.id,is_active =True)
            list.append(product_offer.discount)
        except ObjectDoesNotExist:
            pass
        #setting discount price zero,if we remove any ofers by chance
        #every time we runserver offers will be setted once again        
        x.discount_price=0
        #incase if there is no any offers for this product(if list is empty) 
        if list:
            maxoffer=max(list)#finding minimum amount of offers from category,subcategory,products to apply
            x.discount_percentage=maxoffer#assigning  discount percentage
            x.discount_price=x.price-(x.price*maxoffer/100)#calculating amount after discount
            x.save()
        else:
            pass
    return render(request,'UserSide/index.html',{'products':allproduct,'Categories':allcategory})
            
    