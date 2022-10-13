from django.shortcuts import render,redirect
from django.contrib import messages
from adminone.models import *
from.models import *
from userside.views import*
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='register')
def add_to_wishlist(request,id):
    wish=get_object_or_404(Product,id=id)
    Wishlist.objects.get_or_create(wished_product=wish,user=request.user)
    messages.success(request,'The item is added to your Wishlist')
    return redirect(ViewWishlist)

@login_required(login_url='register')
def ViewWishlist(request):
    user=request.user
    wishlist_list=Wishlist.objects.filter(user=user)
    return render(request,'wishlist.html',{'Wishlist_list':wishlist_list})

@login_required(login_url='register')
def remove_from_wishlist(request,id):
    user=request.user
    remove_item=Wishlist.objects.get(id=id,user=user)
    remove_item.delete()
    # messages.error(request,'The item is removed from  your Wishlist')
    return redirect(ViewWishlist)