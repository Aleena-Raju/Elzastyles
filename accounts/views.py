import email
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from accounts.models import *
from cartapp.models import Address
from userside.views import index
from django.conf import settings
from twilio.rest import Client
from nastylesstore.views import home
from django.contrib.auth.decorators import login_required
from order.models import *
# from xhtml2pdf import pisa
# from django.http import HttpResponse
# from django.template.loader import get_template


# Create your views here.


def signin(request):
    # if 'username' in request.session:
    #     return redirect()

    if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']  
        # usserblockstaus=Account.objects.get(email=request.POST.get('email'))  
        # if usserblockstaus.is_active==True:
            user = authenticate(email=email, password=password)
        
            # print(email)
            # print(password)
        
            if user is not None:
                login(request,user)
                request.session['username'] = user.username
                return redirect(home)
                # phone=Account.objects.get(email=request.POST.get('email'))  
                # phone_number=phone.phone_number
                # account_sid     = settings.ACCOUNT_SID
                # auth_token      = settings.AUTH_TOKEN
                # client = Client(account_sid, auth_token)
                # verification = client.verify \
                #                         .v2 \
                #                         .services(settings.SERVICE_ID) \
                #                         .verifications \
                #                         .create(to=f'{settings.COUNTRY_CODE}{phone_number}', channel='sms')
                # print(verification.status)
                # messages.success(request, 'Otp sent Succesfully to your Registered Mobile number' )
                # return redirect(f'loginotp/{phone.id}/')
            else:
                messages.error(request, "Invalid Credentials")
                print('NOT ABLE TO SIGNIN')
        # else:
        #     messages.error(request,'You are blocked!!')        
    return render(request,'signin.html')
            


def loginotp(request,id):
    if request.method == 'POST':
        user      = Account.objects.get(id=id)
        phone_number=user.phone_number
        otpvalue  = request.POST.get('otp')
        if otpvalue=="":
            messages.error(request,'Enter The Otp!!!')
        else:
            account_sid     = settings.ACCOUNT_SID
            auth_token      = settings.AUTH_TOKEN
            client = Client(account_sid, auth_token)

            verification_check = client.verify \
                                    .v2 \
                                    .services(settings.SERVICE_ID) \
                                    .verification_checks \
                                    .create(to=f'{settings.COUNTRY_CODE}{phone_number}', code=otpvalue)

            print(verification_check.status)
            if verification_check.status=='approved':
                login(request,user)
                request.session['username'] = user.username
                return redirect(home)
            else:
                messages.error(request, "Wrong otp")
    return render(request,'loginotp.html')


def signup(request):
    if request.method =='POST':
        username = request.POST['username']   
        first_name = request.POST['first_name']                
        last_name = request.POST['last_name']                
        email = request.POST['email']                
        phone_number = request.POST['phone_number']                
        password1 = request.POST['password1']                             
        password2 = request.POST['password2']  
        if password1 ==password2:
            if username=="":
                messages.error(request,"username is empty")
                return render(request,'signup.html')              
            elif len(username)<2:
                messages.error(request,"username is too short")
                return render(request,'signup.html')  
            elif not username.isalpha():
                messages.error(request,"username must contain alphabets")
                return render(request,'signup.html')  
            elif not username.isidentifier():
                messages.error(request,"username start must with alphabets")
                return render(request,'signup.html')  
                                
            elif Account.objects.filter(username = username):
                messages.error(request,"username exits")
                return render(request,'signup.html')
            elif email=="":
                messages.error(request,"email field is empty")
                return render(request,'signup.html')
            elif len(email)<2:
                messages.error(request,"email is too short")
                return render(request,'signup.html')
            elif Account.objects.filter(email=email):
                messages.error(request,"email already exist try another")
                return render(request,'signup.html')
                
            else:
                user1 =Account.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password1,email=email,phone_number=phone_number)
                user1.save()
                return redirect(signin)
        else:
            messages.success(request,"password does not match")
            return render(request,'signup.html')
    else:
        return render(request,'signup.html') 
        
    # return render(request,'login-register.html') 
    

@login_required(login_url = 'signin')
def signout(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect(signin)

@login_required(login_url = 'signin')
def dashboard(request):
    addr = Address.objects.filter(user=request.user)
    print(addr,'this is address in user profile......................')
    context = {
        'addresses' : addr
    }
    return render(request, 'usertable.html', context)


def useraddress(request):
    if request.method == "POST":
                Buyername = request.POST["Buyername"]
                Buyers_Address = request.POST["Buyers_Address"]
                email = request.POST["email"]
                phone_number = request.POST["phone_number"]
                country = request.POST["country"]
                city = request.POST["city"]
                state = request.POST["state"]
                pincode = request.POST["pincode"]
                
                if Buyername == "":
                    messages.error(request, "NameField is empty")
                    return render(request, "usertable.html")
                    

                elif len(Buyername) < 2:
                    messages.error(request, "Name is too short")
                    return render(request, "usertable.html")


                elif not Buyername.isalpha():
                    messages.error(request, "Name must contain alphabets")
                    return render(request, "usertable.html")


                elif not Buyername.isidentifier():
                    messages.error(request, "name start must start with alphabets")
                    return render(request, "usertable.html")
                
                elif email == "":
                    messages.error(request, "email field is empty")
                    return render(request, "usertable.html")
                elif len(email) < 2:
                    messages.error(request, "email is too short")
                    return render(request, "usertable.html")
                elif len(phone_number) < 10:
                    messages.error(request, "Mobile Number should be 10 Digits")
                    return render(request, "usertable.html")

                

                elif Address.objects.filter(email=email):
                    messages.error(request, "email already exist try another")
                    return render(request, "usertable.html")
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
                return redirect(dashboard)
    return render(request, 'usertable.html')


def invoice(request, id):
    address = Address.objects.filter(user = request.user)
    order   = Order_Product.objects.filter(id = id)
    context = {
        'address':address,
        'order': order,
        
    }
    return render(request, 'success.html', context)


# def invoice_download(request):
#     if request.method == "POST":
#         order_number = request.POST['order_number']
#         transID = request.POST['payment_id']

#         try:
#             order = Order.objects.get(order_id=order_number, is_ordered=True)
#             ordered_products = Order_Product.objects.filter(order_id=order.id)

#             subtotal = 0
#             for i in ordered_products:
#                 subtotal += i.product_price * i.quantity

#             payment = Payment.objects.get(payment_id=transID)
#             discount_total = ((subtotal + order.tax)-order.order_total )
#             template_path = 'export/invoice_pdf.html' 
#             context = {
#                 'order': order,
#                 'ordered_products': ordered_products,
#                 'order_number': order.order_id,
#                 'transID': payment.payment_id,
#                 'payment': payment,
#                 'subtotal': subtotal,
#                 'discount_total': discount_total,
#             }
        
#             response = HttpResponse(content_type ='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="invoice_report.pdf"'
        
#             template = get_template(template_path)

#             html = template.render(context)

#             # create a pdf
#             pisa_status = pisa.CreatePDF(
#             html, dest=response)
#             # if error then show some funy view
#             if pisa_status.err:
#                 return HttpResponse('We had some errors <pre>' + html + '</pre>')
#             return response
        
#         except (Payment.DoesNotExist, Order.DoesNotExist):
        
#             return redirect('home')
        
        
