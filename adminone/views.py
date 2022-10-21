from django.shortcuts import render

# Create your views here.
from ast import Return
from django.shortcuts import render
import email
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control 
from accounts.models import Account
from category.models import Category
from products.models import *
from order.models import *
from cartapp.models import *
from django.core.paginator import Paginator
import calendar
from datetime import date
import datetime
from django.db.models.functions import ExtractMonth,ExtractYear,ExtractDay
from django.db.models import Max,Min,Count,Avg,Sum
from extra.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



# Create your views here.
@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def signinadmin(request):
    if 'username' in request.session:
        return redirect(admin_home)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email = email,password=password)
        print ('ffffffff')
        if user is not None:
            if user.is_superuser:
                request.session['username']=email
                login(request,user)
                return redirect(admin_home)
        else:
            messages.error(request,'invalid credentials')
            return redirect(signinadmin)

    return render (request,'adminlogin.html')


@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def admin_home(request):
    return render (request,'admindashboard.html')

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def admin_logout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(signinadmin) 

def user_list(request):
    theuser = Account.objects.all()
    return render (request,'userlist.html',{'theuser':theuser})   

def block_user(request,id):
    x=Account.objects.get(id=id)
    if x.is_active:
        x.is_active=False
    else:
        x.is_active=True
    x.save()         
    return redirect(user_list)

def product(request):
    theproduct = Product.objects.all()
    paginator  = Paginator(theproduct, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    return render (request,'product.html',{'theproduct':paged_products})

def deleteproduct(request,id):
    deleteproduct =Product.objects.get(id=id)
    deleteproduct.delete()
    return redirect(product)


def addproduct(request):
    values = Category.objects.all()
    if request.method =='POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        x = Category.objects.get(id=category)
        prod=Product(product_name=name,slug=name,description=description,price=price,stock=stock,category=x,image1=image1,image2=image2,image3=image3)
    
        prod.save()
        return redirect(product)
        
    return render(request,'Addproduct.html',{'values':values})  



# def editproduct(request,id):
#     this_product = Product.objects.get(id=id)
#     return render(request,'productuser.html',{'this_product': this_product,})      

    
def editproduct(request,id):
    this_product = Product.objects.get(id=id)
    values = Category.objects.all()

    if request.method == 'POST':

        product_name = request.POST.get('name')
        product_description = request.POST.get('description')
        product_price = request.POST.get('price')
        product_stock = request.POST.get('stock')
        product_image1 = request.POST.get('image1')
        product_image2 = request.POST.get('image2')
        product_image3 = request.POST.get('image3')
        obj = Product.objects.get(id=id)
        obj.name = product_name
        obj.description = product_description
        obj.price = product_price
        obj.stock = product_stock
        obj.image1 = product_image1
        obj.image2 = product_image2
        obj.image3 = product_image3

        obj.save()
        return redirect(product)
    return render(request,'editproduct.html',{'this_product': this_product,'values':values})      

@cache_control(no_cache =True, must_revalidate =True, no_store =True)
def categoryList(request):
    if 'username' in request.session:
        values = Category.objects.all()
        return render(request,'categories.html',{'values':values})
    return redirect(signinadmin)
    
def addcategory(request):
    values = Category.objects.all()
    if request.method =='POST':
        name = request.POST.get('name')
        if Category.objects.filter(category_name__icontains=name).exists():
            messages.error(request, "This Category  already Exists")
            print('This category exits')
            return redirect(addcategory)
        description = request.POST.get('description')
        variables = Category(category_name=name,slug=name,description=description)
    
        variables.save()
        
    return render(request,'Addcategory.html')      

def deletecategory(request,id):
    my_cat = Category.objects.get(id=id)
    my_cat.delete()
    return redirect(categoryList) 



def Adminvieworder_Details(request):
   orderproductdetails=Order_Product.objects.all()
   paginator=Paginator(orderproductdetails,5)
   page_number=request.GET.get('page')
   orderproductdetailsFinal=paginator.get_page(page_number)
#    totalpage=orderproductdetailsFinal.paginator.num_pages
   context={
        'OrderProductDetails': orderproductdetailsFinal, 
        # 'lastpage':totalpage,
        # 'totalPagelist':[ n+1 for n  in range(totalpage)]

    }

   return render(request,'OrderList.html',context)  



def order_Cancelled(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Cancelled'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(Adminvieworder_Details)

def order_Shipped(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Shipped'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(Adminvieworder_Details)

def order_Out_For_delivery(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Out for delivery'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(Adminvieworder_Details)


def order_Delivered(request,id):
    user=request.user
    orderproductdetails=Order_Product.objects.get(id=id)
    print(orderproductdetails.status)
    orderproductdetails.status='Delivered'
    print('------------------')
    orderproductdetails.save()
    print(orderproductdetails.status)

    return redirect(Adminvieworder_Details)



def adminDashboard(request):

    orders=Order.objects.annotate(month=ExtractMonth('date')).values('month').annotate(count=Count('id')).values('month','count')
    yearorders=Order.objects.annotate(year=ExtractYear('date')).values('year').annotate(count=Count('id')).values('year','count')
    Dayorders=Order.objects.annotate(day=ExtractDay('date')).filter(date=date.today()).values('day').annotate(count=Count('id')).values('day','count')
    # print(request.user.is_admin)

    
    print(Dayorders)
    DayNumber=[]
    YearNumber=[]
    monthNumber=[]
    totalOrders=[]
    totaltyearorders=[]
    totaldayorder=[]
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])

    for d in yearorders:
        YearNumber.append([d['year']])
        totaltyearorders.append(d['count'])
    
    for d in Dayorders:
        DayNumber.append([d['day']])
        totaldayorder.append(d['count'])

    # ---------------------------------- payment --------------------------------- #
    Allorders = Order.objects.all()
    # orderproduct = OrderProduct.objects.filter(product__category_name = 1)
    

    # codtotal = Payment.objects.filter(payment_method = 'cashondelivery').aggregate(Sum('amount')).get('amount__sum')
    cod = Payment.objects.filter(payment_method = 'cashondelivery').aggregate(Count('id')).get('id__count')
       
    # raztotal = Payment.objects.filter(payment_method = 'razorpay').aggregate(Sum('amount')).get('amount__sum')
    raz = Payment.objects.filter(payment_method = 'razorpay').aggregate(Count('id')).get('id__count')

    # paypaltotal = Payment.objects.filter(payment_method = 'Paypal').aggregate(Sum('amount')).get('amount__sum')
    pay = Payment.objects.filter(payment_method = 'paypal').aggregate(Count('id')).get('id__count')

    # ordertotal = Payment.objects.all().aggregate(Sum('amount')).get('amount__sum')

    # --------------------------------- StockLeft -------------------------------- #
    

    
    context={
        'Order':orders,
        'MonthNumber':monthNumber,
        'TotalOrders':totalOrders,
        'YearNumber':YearNumber,
        'totaltyearorders':totaltyearorders,
        'DayNumber':DayNumber,
        'totaldayorder':totaldayorder,
        'Allorders':Allorders,
        #'codtotal':codtotal,
        #'paypaltotal':paypaltotal,
        #'raztotal':raztotal,
        #'total':ordertotal,
        'paypal':pay,
        'raz':raz,
        'cod':cod

    }
    return render(request,'admindashboard.html',context)




# ------------------------------ Sales Report------------------------------ #
# --------------------------- sales report-------------------------- #

def salesreport(request):
    salesreport = Order.objects.all().order_by('-id')
    
    if request.method  == 'POST':
        search = request.POST["salesreport_search"]
        salesreports = Order.objects.filter(order_id__contains = search)
        context = {
            'salesreport':salesreports,
        }
        return render (request,"salesreport.html",context)

    context = {
            'salesreport':salesreport,
        }
    return render (request,"salesreport.html",context)


# --------------------------- date-------------------------- #

def date_range(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        if len(fromdate)>0 and len(todate)> 0 :
            frm = fromdate.split("-")
            tod = todate.split("-")

            fm = [int(x) for x in frm]
            todt = [int(x) for x in tod]

            salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2]) )
            context = {
                'salesreport':salesreport,
            }

            return render(request,'salesreport.html',context)

        else:
            salesreport = Order.objects.all()
            context = {
                'salesreport': salesreport ,
                

            
            }
            


    return render (request,"salesreport.html",context)
        
# --------------------------- monthly report-------------------------- #


def monthly_report(request,date):
    frmdate = date
    fm = [2022, frmdate, 1]
    todt = [2022,frmdate,30]

    salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2])).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'salesreport.html')

# --------------------------- yearly sales report-------------------------- #

def yearly_report(request,date):
    frmdate = date
    fm = [frmdate, 1, 1]
    todt = [frmdate,12,31]

    salesreport = Order.objects.filter(date__gte = datetime.date(fm[0],fm[1],fm[2]),date__lte=datetime.date(todt[0],todt[1],todt[2])).order_by("-id")
    if len(salesreport)>0:
        context = {
            'salesreport':salesreport,
        }
        return render(request,'salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'salesreport.html')   
    
    
    

# ------------------------------ Coupon Offer ------------------------------ #
# --------------------------- viewcoupon offer -------------------------- #
def view_coupon(request):
    coupons =Coupon.objects.all().order_by("id")
    return render(request, "view_coupon.html",{"coupons":coupons})

# --------------------------- usedcoupon -------------------------- #

def view_couponuseduser(request):
    coupon_useduser=UsedCoupon.objects.all().order_by("id")
    return render(request, "view_couponuseduser.html",{"coupon_useduser:coupon_useduser"})

# --------------------------- addcoupon-------------------------- #
# addcoupons

def add_coupon(request):
    if request.method == "POST":
        coupon_code =request.POST.get("coupon_code")
        discount_percentage =request.POST.get("discount_price")
   
        try:
            discount= int(discount_percentage)
            if discount > 0 :
                if discount <100:
                    coupons=Coupon(coupon_code=coupon_code,discount_percentage=discount)
                    coupons.save()
                    print("coupon",coupon_code)
                    return redirect(view_coupon)
        except:
            messages.success(request,"cant repeat same coupon and offer must be between 1 to 90%")
            return render(request, "add_coupon.html")

    return render(request, "add_coupon.html")

# ---------------------------addcoupon -------------------------- #

def block_coupon(request, id):
    coupons = Coupon.objects.get(id=id)
    if coupons.is_active:
        coupons.is_active = False
    else:
        coupons.is_active = True
    coupons.save()
    return redirect(view_coupon)

# --------------------------- delete coupon-------------------------- #

def delete_coupon(request,id):
    coupons = Coupon.objects.get(id=id)
    coupons.delete()
    return redirect(view_coupon) 

# ------------------------------ Category Offer ------------------------------ #
# --------------------------- Adding category offer -------------------------- #

def New_CategoryOffer(request):
    CategoryObj=Category.objects.all()
    if request.method=="POST":
        discount=request.POST.get("discount")
        category=request.POST.get("category_name")
        discount=int(discount)
        if Categoryoffer.objects.filter(category=category).exists():
            messages.error(request,"Offer already exists for this Category")
            return redirect(View_CategoryOffers)
        if discount>0:
            if discount<90:
                
                newCategoryOffer=Categoryoffer()
                newCategoryOffer.discount=discount
                newCategoryOffer.category=Category.objects.get(id=category)
                newCategoryOffer.save()
                return redirect(View_CategoryOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_CategoryOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_CategoryOffer)
    return render(request,'Add_NewCategoryOffer.html',{'Category':CategoryObj})

# ---------------------------- Edit CategoryOffer ---------------------------- #

def Edit_CategoryOffer(request,id):
    CategoryObj=Category.objects.all()
    CategoryOfferObj=Categoryoffer.objects.get(id=id)
    if request.method=="POST":
        discount=request.POST.get("discount")
        category=request.POST.get("category_name")
        discount=int(discount)
        if discount>0:
            if discount<90:
                CategoryOfferObj.discount=discount
                CategoryOfferObj.category=Category.objects.get(id=category)
                CategoryOfferObj.save()
                return redirect(View_CategoryOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_CategoryOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_CategoryOffer)
    context={
        'Category':CategoryObj,
        'CategoryOffer':CategoryOfferObj
    }
    return render(request,'Edit_CategoryOffer.html',context)



# --------------------------- View category Offers --------------------------- #
def View_CategoryOffers(request):
    CategoryOfferObj=Categoryoffer.objects.all()
    paginator=Paginator(CategoryOfferObj,per_page=2)
    page_number=request.GET.get('page')
    CategoryOfferObjfinal=paginator.get_page(page_number)
    totalpage=CategoryOfferObjfinal.paginator.num_pages
    context={
        'CategoryOffer':CategoryOfferObjfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }
    return render(request,'View_CategoryOffer.html',context)

# -------------------------- Delete A Category Offer ------------------------- #
def Delete_CategoryOffer(request,id):
    toDelete_CategoryOffer=Categoryoffer.objects.get(id=id)
    toDelete_CategoryOffer.delete()
    messages.success(request,'Offer Deleted successfully')
    return redirect(View_CategoryOffers)

# ---------------------------- Block CategoryOffer --------------------------- #
def Block_CategoryOffer(request,id):
    toBlock_CategoryOffer=Categoryoffer.objects.get(id=id)
    toBlock_CategoryOffer.is_active=False
    toBlock_CategoryOffer.save()
    messages.error(request, 'Offer is Blocked Successfully')
    return redirect(View_CategoryOffers)

# --------------------------- Unblock CategoryOffer -------------------------- #
def UnBlock_CategoryOffer(request,id):
    toUnBlock_CategoryOffer=Categoryoffer.objects.get(id=id)
    toUnBlock_CategoryOffer.is_active=True
    toUnBlock_CategoryOffer.save()
    messages.error(request, 'Offer is UnBlocked Successfully')
    return redirect(View_CategoryOffers)    

# ------------------------------ Product Offer ------------------------------ #
# --------------------------- Adding Product  offer -------------------------- #

def New_ProductOffer(request):
    products=Product.objects.all()
    if request.method=="POST":
        discount=request.POST.get("discount")
        choosed_product=request.POST.get("product_name")
        if Productoffer.objects.filter(product=choosed_product).exists():
            messages.info(request,"Offer already exists for this Product")
            return redirect(View_ProductOffers)
        discount=int(discount)
        if discount>0:
            if discount<90:
                newProductOffer=Productoffer()
                newProductOffer.discount=discount
                # newProductOffer.product=Product.objects.get(id=choosed_product)
                product=Product.objects.get(id=choosed_product)
                product.discount_price=(product.price-(product.price*discount/100))
                print('product',product.discount_price)
                product.save()
                print('product',product.discount_price)
                newProductOffer.product=Product.objects.get(id=choosed_product)
                newProductOffer.save()
                return redirect(View_ProductOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(New_ProductOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(New_ProductOffer)
    return render(request,'Add_NewProductOffer.html',{'Products':products})

# # ---------------------------- Edit ProductOffer ---------------------------- #

def Edit_ProductOffer(request,id):
    products=Product.objects.all()
    ProductOfferObj=Productoffer.objects.get(id=id)
    if request.method=="POST":
        discount=request.POST.get("discount")
        choosed_product=request.POST.get("product_name")
        discount=int(discount)
        if discount>0:
            if discount<90:
                ProductOfferObj.discount=discount
                ProductOfferObj.category=Product.objects.get(id=choosed_product)
                ProductOfferObj.save()
                return redirect(View_ProductOffers)
            else:
                messages.error(request,"Discount must be less than 90%")
                return redirect(Edit_ProductOffer)
        else:
                messages.error(request,"Discount must be greater than 0%")
                return redirect(Edit_ProductOffer)
    context={
        'Products':products,
        'ProductOfferObj':ProductOfferObj
    }
    return render(request,'Edit_ProductOffer.html',context)



# # --------------------------- View Product Offers --------------------------- #
def View_ProductOffers(request):
    ProductOfferObj=Productoffer.objects.all()
    paginator=Paginator(ProductOfferObj,per_page=2)
    page_number=request.GET.get('page')
    ProductOfferObjfinal=paginator.get_page(page_number)
    totalpage=ProductOfferObjfinal.paginator.num_pages
    context={
        'ProductOffer':ProductOfferObjfinal,
        'lastpage':totalpage,
        'totalPagelist':[ n+1 for n  in range(totalpage)]

    }
    return render(request,'View_ProductOffer.html',context)


# -------------------------- Delete A Product Offer ------------------------- #
def Delete_ProductOffer(request,id):
    toDelete_ProductOffer=Productoffer.objects.get(id=id)
    
    toDelete_ProductOffer.delete()
    messages.success(request,'Offer Deleted successfully')
    return redirect(View_ProductOffers)

# ---------------------------- Block ProductOffer --------------------------- #
def Block_ProductOffer(request,id):
    toBlock_ProductOffer=Productoffer.objects.get(id=id)
    toBlock_ProductOffer.is_active=False
    toBlock_ProductOffer.save()
    messages.error(request, 'Offer is Blocked Successfully')
    return redirect(View_ProductOffers)

# --------------------------- Unblock ProductOffer -------------------------- #
def UnBlock_ProductOffer(request,id):
    toUnBlock_ProductOffer=Productoffer.objects.get(id=id)
    toUnBlock_ProductOffer.is_active=True
    toUnBlock_ProductOffer.save()
    messages.error(request, 'Offer is UnBlocked Successfully')
    return redirect(View_ProductOffers)    
