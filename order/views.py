from django.shortcuts import render,redirect
from order.models import*
from cartapp.models import*
from accounts.models import*
from cartapp.views import*
from accounts.views import*
from django.views.decorators.csrf import csrf_exempt
from order.models import*
import razorpay
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator




# Create your views here.
from datetime import date
import datetime


# Create your views here.
def vieworder_Details(request):
    
    user=request.user
    order=Order_Product.objects.filter(user=user)
    paginator = Paginator(order,4)
    page = request.GET.get('page')
    paged_Order  = paginator.get_page(page)
    order_count = order.count()
    context = {
            'order': paged_Order,
            'order_count': order_count,
        }
    return render(request,'ordermanegement.html',context)


def Cancelorder(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='cancelled'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(vieworder_Details)

def returnorder(request,id):
    if request.user is not None:
        orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Returned'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(vieworder_Details)

def PlaceOrder(request):
    request.session['OrderId']=None
    if request.method=='POST':
        pay_mode=request.POST['payment-method']
        address_buyer=request.POST['addressUsed']
        if pay_mode=="":
            messages.error(request,"Choosing A Payment Method is Mandatory")
            return redirect(PlaceOrder)
        if address_buyer=="":
            messages.error(request,"Please Choose Your Address")
            return redirect(PlaceOrder)
        print(address_buyer)
        global addressdetails#to access it everywhere
        addressdetails=Address.objects.get(id=address_buyer)
        print(addressdetails.Buyername)
    if pay_mode=='cash':
        return redirect(CashonDelivery)
    if pay_mode=='RazorPay':
        return redirect(razorPayPayment)         
    if pay_mode=='PayPal':
        return redirect(payPalPayment)
    return render (request,"success.html")


def CashonDelivery(request):
        if 'coupon_code' in request.session:
            coupon_code = request.session['coupon_code']
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            reduction = coupon.discount_percentage
        else:
            reduction = 0
        user = request.user
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request)) 
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
        cart_itemcount = cartlist_items.count()
        print(cart_itemcount)
        if request.user.is_authenticated:
            total=0
            quantity=0
            count=0
            for i in cartlist_items:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
            tax = (2 * total)/100
            total=tax+total - reduction*total/100
            # ------------------ saving Whole Order Payment details of CashonDelivey ----------------- #
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="cashondelivery"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()
            # ------------------ saving Whole Order details of CashonDelivey ----------------- #
            Obj_Order=Order()
            
        
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
            Obj_Order.is_ordered=True
            Obj_Order.save() 
            # ------------------ saving each product Order details of CashonDelivey ----------------- #
            for x in cartlist_items:
                orderproduct = Order_Product()
                orderproduct.user=request.user
                orderproduct.order=Obj_Order
                orderproduct.quantity =x.quantity
                orderproduct.product=x.product
                orderproduct.payment=payment_obj
                orderproduct.product_price=x.product.price

                orderproduct.save() 
                request.session['OrderId']=orderproduct.id
                id=orderproduct.id
                product = Product.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()
            cartlist_items.delete()
            
            return redirect(orderConfirmed)
        
def orderConfirmed(request):
    id=request.session['OrderId']
    if 'coupon_code' in request.session:
        coupon_code = request.session['coupon_code']
        coupon = Coupon.objects.get(coupon_code = coupon_code)
        reduction = coupon.discount_percentage
    else:
        reduction = 0 
    try:
        if 'coupon_code' in request.session:
            coupon_used  = UsedCoupon(coupon = coupon, user = request.user)
            coupon_used.save()
    except:
        pass
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        return redirect(invoice,id)
    return redirect(invoice,id)
def razorPayPayment(request):
    if 'coupon_code' in request.session:
        coupon_code = request.session['coupon_code']
        coupon = Coupon.objects.get(coupon_code = coupon_code)
        reduction = coupon.discount_percentage
    else:
        reduction = 0
        print("HI razor")
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        global cartlist_items
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
        print(cart_itemsid)
        print(cartlist_items)
        cart_itemcount = cartlist_items.count()
        print(cart_itemcount)
        if request.user.is_authenticated:
            total=0
            quantity=0
            count=0            
            for i in cartlist_items:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity    
            subtotal=total            
            tax = ((2 * total)/100)
            amount=tax+total - reduction*total/100
            amount=int(amount)*100           
            print(amount) 

            global payment_obj
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="razorpay"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()





            global Obj_Order
            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
 
            Obj_Order.save()

            for x in cartlist_items:
                orderproduct = Order_Product()
                orderproduct.user=request.user
                orderproduct.order=Obj_Order
                orderproduct.quantity =x.quantity
                orderproduct.product=x.product
                orderproduct.payment=payment_obj
                orderproduct.product_price=x.product.price
                orderproduct.save() 
                product = Product.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()
                request.session['OrderId']=orderproduct.id

                
            
        if request.method == "POST":

            client = razorpay.Client(auth=("rzp_test_YvJpGLS6WYeGXf", "9pMx6a3ciw1EWN8brd8KAEAz"))
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            print(payment)
            return render(request,'razorpay.html',{'payment': payment}) 
    return render(request,'razorpay.html') 

    # def razorPayPayment(request):
    
    # address_buyer=request.POST['addressUsed']
    # print(address_buyer)
    # addressdetails=Address.objects.get(id=address_buyer)
    # print(addressdetails.Buyername)
    
    # print("HI razor")
    # cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
    # global cartlist_items
    # cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)
    # print(cart_itemsid)
    # print(cartlist_items)
    # cart_itemcount = cartlist_items.count()
    # print(cart_itemcount)
    # if request.user.is_authenticated:
    #     total=0
    #     quantity=0
    #     count=0
    #     rawtotal=0            
    #     for i in cartlist_items:
    #             if i.product.discount_price>0:
    #                 total+=(i.product.discount_price*i.quantity)
    #                 count+=i.quantity
    #             else:
    #                 total+=(i.product.price*i.quantity)
    #                 count+=i.quantity
    #             rawtotal+=(i.product.price*i.quantity) 
    #     print(rawtotal)#without discount    
    #     subtotal=total
    #     print('after discount')
    #     print(subtotal)#with discount
    #     tax = (2 * subtotal)/100
    #     # alltotal=tax+subtotal#after having tax   
    #     alltotal=request.session['Totalamount']

    #     amount=alltotal*100   
    #     amount=int(amount)        
    #     print(amount) 

    #     global payment_obj
    #     payment_obj=Payment()
    #     payment_obj.user=request.user
    #     payment_obj. payment_method="razorpay"
    #     payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    #     payment_obj.date =date.today()
    #     payment_obj.amount=alltotal
    #     payment_obj.save()





    #     global Obj_Order
    #     Obj_Order=Order()
    #     Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    #     Obj_Order.date =date.today()
    #     Obj_Order.user=request.user
    #     Obj_Order.total=alltotal
    #     Obj_Order.address=addressdetails
    #     Obj_Order.payment=payment_obj
        
        
    #     Obj_Order.save()

    #     for x in cartlist_items:
    #         orderproduct = Order_Product()
    #         orderproduct.user=request.user
    #         orderproduct.order=Obj_Order
    #         orderproduct.quantity =x.quantity
    #         orderproduct.product=x.product
    #         orderproduct.payment=payment_obj
    #         orderproduct.product_price=x.product.price
    #         orderproduct.save() 
    #         product = Product.objects.get(id = x.product.id)
    #         product.stock -= x.quantity
    #         product.save()
    # if request.method == "POST":
    #     client = razorpay.Client(auth=("rzp_live_javdJVeqtD5cfZ", "4GS5XjEzRNExDTCGkKm2rms8"))
    #     print('hellooo')
    #     payment = client.order.create({'amount': amount*100, 'currency': 'INR', 'payment_capture': '1'})        
    #     return render(request,'Order_Confirm.html',{'payment': payment,'amount':amount})   
    # return render(request,'Order_Confirm.html',{'amount':amount})

def success(request):
    id=request.session['OrderId']
    if 'coupon_code' in request.session:
        coupon_code = request.session['coupon_code']
        coupon = Coupon.objects.get(coupon_code = coupon_code)
        reduction = coupon.discount_percentage
    else:
        reduction = 0
    payment_obj.payment_status="Payment Succesfull"
    payment_obj.save(update_fields=['payment_status'])
    print('updated paymentstatus')
    Obj_Order.is_ordered=True
    Obj_Order.save(update_fields=['is_ordered'])
    try:
        if 'coupon_code' in request.session:
            coupon_used  = UsedCoupon(coupon = coupon, user = request.user)
            coupon_used.save()
    except:
        pass
    if 'coupon_code' in request.session:
        del request.session['coupon_code']

    cartlist_items.delete()
    print('deleted from cart')
    return redirect(invoice,id)

def payPalPayment(request):
        print("HI paypal")
        if 'coupon_code' in request.session:
            coupon_code = request.session['coupon_code']
            coupon = Coupon.objects.get(coupon_code = coupon_code)
            reduction = coupon.discount_percentage
        else:
            reduction = 0
        user = request.user
        print(user)
        cart_itemsid=Cart.objects.get(cart_id=create_cart_id(request))
        global cartlist_items
        cartlist_items=Cart_Products.objects.filter(cart=cart_itemsid,is_active=True)

        print(cart_itemsid)
        print(cartlist_items)

        cart_itemcount = cartlist_items.count()
        print(cart_itemcount)
        

        if request.user.is_authenticated:
       
            total=0
            quantity=0
            count=0
            
            for i in cartlist_items:
                    total+=(i.product.price*i.quantity)
                    count+=i.quantity
    
            subtotal=total
            
            tax = (2 * total)/100
            total=tax+total - reduction*total/100
            
            print(total)
            print('printed')
            global payment_obj
            payment_obj=Payment()
            payment_obj.user=request.user
            payment_obj. payment_method="paypal"
            payment_obj.payment_id = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            payment_obj.date =date.today()
            payment_obj.amount=total
            payment_obj.save()





            global Obj_Order
            Obj_Order=Order()
            Obj_Order.order_id= str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            Obj_Order.date =date.today()
            Obj_Order.user=request.user
            Obj_Order.total=total
            Obj_Order.address=addressdetails
            Obj_Order.payment=payment_obj
            Obj_Order.is_ordered=True
            Obj_Order.save()
            order = get_object_or_404(Order, id=Obj_Order.id)
            host = request.get_host()

            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': total,
                'item_name': 'Order {}'.format(order.id),
                'invoice': str(order.id),
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
                'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
            }
            form = PayPalPaymentsForm(initial=paypal_dict)
            
            
            
            print("hello")
           
            for x in cartlist_items:
                orderproduct = Order_Product()

                orderproduct.user=request.user
                orderproduct.order=Obj_Order
                orderproduct.quantity =x.quantity
                orderproduct.product=x.product
                orderproduct.payment=payment_obj
                orderproduct.product_price=x.product.price
                orderproduct.save() 
                product = Product.objects.get(id = x.product.id)
                product.stock -= x.quantity
                product.save()
                request.session['OrderId']=orderproduct.id
                
            cartlist_items.delete()
            print('deleted from cart')
            return render (request,'paypal.html',{'total':total,'order': order,'form': form}) 
# @csrf_exempt
# def success(request):
#     return render(request, "success.html")


@csrf_exempt
def payment_done(request):
    id=request.session['OrderId']
    if 'coupon_code' in request.session:
        coupon_code = request.session['coupon_code']
        coupon = Coupon.objects.get(coupon_code = coupon_code)
        reduction = coupon.discount_percentage
    else:
        reduction = 0
    payment_obj.payment_status="Payment Succesfull"
    payment_obj.save(update_fields=['payment_status'])
    print('updated paymentstatus')
    Obj_Order.is_ordered=True
    Obj_Order.save(update_fields=['is_ordered'])
    cartlist_items.delete()
    print('deleted from cart')
    try:
        if 'coupon_code' in request.session:
            coupon_used  = UsedCoupon(coupon = coupon, user = request.user)
            coupon_used.save()
    except:
        pass
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    return redirect(invoice,id)


@csrf_exempt
def payment_canceled(request):
    return redirect(view_cart)




