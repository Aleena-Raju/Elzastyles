from email import message
from http import client
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
import json
import random
import re
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import datetime
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, render
from products.models import *
from accounts.models import *
from cartapp.models import *
from extra.models import *
from django.http import HttpResponse
from django.contrib import auth
# from orders.models import OrderProduct, Orders, Payment
from datetime import date 
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.






# ----------------- creating separate sessions for each user----------------- #
def create_cart_id(request):
    cartlist_id=request.session.session_key
    if not  cartlist_id:
        cartlist_id=request.session.create()
    return cartlist_id




# ---------------------- funtionality for adding to cart --------------------- #
def add_ToCart(request,id):
    #product is adding with its id 
    product=Product.objects.get(id=id)
    if request.user.is_authenticated:
        #if there is chance to have error
        try:
            cart__id=Cart.objects.get(cart_id=create_cart_id(request))#took sessionkeyif it is exists
        except Cart.DoesNotExist:
            cart__id=Cart.objects.create(cart_id=create_cart_id(request))#created sessionkey if it doesnot exists  
            cart__id.save()
        # to take objects from Cart_Products
        try:
            cart_items=Cart_Products.objects.get(product=product,cart=cart__id,user=request.user)
            if cart_items.quantity<cart_items.product.stock:#checking quantity with stock
                cart_items.quantity+=1#increasing the quantity 
                cart_items.save()
            else:
                return JsonResponse({'msg':'fail'})
        except Cart_Products.DoesNotExist:#not available,create one
            cart_items=Cart_Products.objects.create(product=product,quantity=1,cart=cart__id,user=request.user)
            cart_items.save()
        return redirect('ViewCart')
    else : 
        try:
            cart__id=Cart.objects.get(cart_id=create_cart_id(request))#took sessionkeyif it is exists
        except Cart.DoesNotExist:
            cart__id=Cart.objects.create(cart_id=create_cart_id(request))#created sessionkey if it doesnot exists  
            cart__id.save()
        # to take objects from Cart_Products
        try:
            cart_items=Cart_Products.objects.get(product=product,cart=cart__id)
            if cart_items.quantity<cart_items.product.stock:#checking quantity with stock
                cart_items.quantity+=1#increasing the quantity 
            cart_items.save()
        except Cart_Products.DoesNotExist:#not available,create one
            cart_items=Cart_Products.objects.create(product=product,quantity=1,cart=cart__id)
            cart_items.save()
        return redirect('ViewCart')



#------------------------ list the items in the cart ------------------------ #
def view_cart(request,total=0,count=0,cartlist_items=None):
    if 'coupon_code' in request.session:
        coupon_code = request.session['coupon_code']
        coupon = Coupon.objects.get(coupon_code = coupon_code)
        reduction = coupon.discount_percentage
    else:
        reduction = 0
    try:
        if request.user.is_authenticated:
            cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
            cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True,user=request.user)
            for i in cartlist_items:
                        total+=(i.product.price*i.quantity)
                        count+=i.quantity
        else:
            cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
            cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
            for i in cartlist_items:
                        total+=(i.product.price*i.quantity)
                        count+=i.quantity
    except ObjectDoesNotExist:
        pass
    subtotal=total
    tax = (2 * total)/100
    total=tax+total - reduction*total/100
    print(cartlist_items,"llllllllll")
    return render(request,'shoping-cart.html',{'Cart_items':cartlist_items,'Total':total,'Count':count,'Tax':tax,'Subtotal':subtotal})




# ----------------------- decrease the quantity in cart ---------------------- #
def decrease_quantity_cart(request,id):
    cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
    product=get_object_or_404(Product,id=id)#this will find the object from mentioned model ,in a given certain conditions
    cart_items=Cart_Products.objects.get(product=product,cart=cart_itemsid,user=request.user)
    if cart_items.quantity>1:
        cart_items.quantity-=1
        cart_items.save()
    else:
        pass
    return redirect(view_cart)




# # ------------------------- delete product from cart ------------------------- #
# def delete_product_cart(request,id):
#     cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
#     product=get_object_or_404(Product,id=id)#this will find the object from mentioned model ,in a given certain conditions
#     cart_items=Cart_Products.objects.get(product=product,cart=cart_itemsid)
#     cart_items.delete()
#     return redirect(view_cart)









@login_required(login_url = 'register')
def add_address(request):
        total=0
        count=0
        cartlist_items=None
    

        if request.user.is_authenticated:
            try:
                cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
                cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True,user=request.user)
                for i in cartlist_items:
                            total+=(i.product.price*i.quantity)
                            count+=i.quantity
            except ObjectDoesNotExist:
                pass
            subtotal=total
            tax = (2 * total)/100
            total=tax+total
            addressDetails = Address.objects.filter(user=request.user)
        if request.method == "POST":
                Buyername = request.POST["Buyername"]
                Buyers_Address = request.POST["Buyers_Address"]
                email = request.POST["email"]
                phone_number = request.POST["phone_number"]
                country = request.POST["country"]
                city = request.POST["city"]
                state = request.POST["state"]
                pincode = request.POST["pincode"]

                address_data = Address(
                        Buyername=Buyername,
                        email=email,
                        phone_number=phone_number,
                        Buyers_Address=Buyers_Address,
                        city=city,
                        state=state,
                        country=country,
                        user=request.user,
                        pincode=pincode
                    )
                address_data.save()
                return redirect(add_address)
        
        return render(request,'AddressAdd.html', {'Cart_items':cartlist_items,'Total':total,'Count':count,'Tax':tax,'Subtotal':subtotal,'AddressDetails':addressDetails})


def delete_product_cart(request,id):
    # if request.method=='POST':
        print('helloooiiiiiiiiiiiiiiiiiiiiiiiii')
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        product=get_object_or_404(Product,id=id)#this will find the object from mentioned model ,in a given certain conditions
        cart_items=Cart_Products.objects.get(product=product,cart=cart_itemsid,user=request.user)
        messages.error(request,'Product is Removed From Cart')
        cart_items.delete()    
        return redirect(view_cart)
    
def coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        print(coupon_code,"This is coupon code")
        try:
            if Coupon.objects.get(coupon_code = coupon_code):
                exists = Coupon.objects.get(coupon_code = coupon_code)
                try:
                    if UsedCoupon.objects.get(user = request.user, coupon = exists):
                        messages.error(request, 'Coupon has already been used')
                        return redirect(view_cart)
                except:
                    request.session['coupon_code'] = coupon_code
                    messages.success(request, 'Your Coupon has been applied')
            else:
                messages.error(request, 'The coupon you entered is invalid')
                return redirect(view_cart)
        except:
            messages.error(request, 'The coupon you entered is invalid')
    return redirect(view_cart)