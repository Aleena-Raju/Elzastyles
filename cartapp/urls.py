from django.urls import path
from . import views

urlpatterns = [

    # path('',views.cartview, name='cartview'),  
    # path('add_cart/<int:id>/',views.add_cart, name='add_cart'),
    
    # # path('add_cartsimple/<int:product_id>/',views.add_cartsimple, name='add_cartsimple'), 

    # path('remove_cart/<int:product_id>/',views.remove_cart,name ='remove_cart' ),
    # path('delete/<int:product_id>/',views.delete_cart,name ='delete_cart' ),
    # path('deleteloggedin/<int:product_id>/',views.delete_cart_loggedin,name ='deleteloggedin' ),

    # --------------------------- View Products in Cart -------------------------- #
    path('',views.view_cart,name='ViewCart'),
    path('addtocart/<int:id>',views.add_ToCart,name='AddToCart'),
    path('decrease_qty/<int:id>',views.decrease_quantity_cart,name='DecreaseQty'),
    path('deletefromcart/<int:id>',views.delete_product_cart,name='DeleteFromCart'),

    
    
  
  # ----------------------------- checkout happens ----------------------------- #

    path('address',views.add_address,name='AddressAdd'),
    
    
    
  # --------------------------Coupon--------------------------------
  path('ApplyCoupon/', views.coupon , name='ApplyCoupon'),

]