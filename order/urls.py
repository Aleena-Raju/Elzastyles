from django.urls import path
from . import views
urlpatterns = [


    
    # --------------------------- OrderManagement -------------------------- #
    path('vieworderdetails',views.vieworder_Details,name='ViewOrderDetails'),
    path('cancelorder/<int:id>',views.Cancelorder,name='Cancelorder'),
    path('returnorder/<int:id>',views.returnorder,name='returnorder'),


    path('placeorder',views.PlaceOrder,name='PlaceOrder'),
    path('CashonDelivery',views.CashonDelivery,name='CashonDelivery'),
    path('payPalPayment',views.payPalPayment,name='PayPalPayment'),
    path('razorPayPayment',views.razorPayPayment,name='RazorPayPayment'),
    path('success',views.success,name='success'),
    path('orderconfirmed',views.orderConfirmed,name='OrderConfirmed'),

    
    path('payment-done/',views.payment_done,name='payment_done'),
    path('payment-cancelled/',views.payment_canceled,name='payment_cancelled'),
    
    
    


]