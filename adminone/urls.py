from collections import UserList
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.signinadmin,name='signinadmin'),
    path('adminhome',views.admin_home,name='adminhome'),
    path('adminlogout',views.admin_logout,name='adminlogout'),
    path('userlist' ,views.user_list,name='userlist'),
    path('blockuser/<int:id>/',views.block_user,name='blockuser'),
    path('product',views.product,name='product'),
    path('editproduct/<int:id>/',views.editproduct,name='blockuser'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('categoryList',views.categoryList,name='category'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('deletecategory/<int:id>/',views.deletecategory,name='deletecategory'),
    path('delete/<int:id>/',views.deleteproduct,name='deleteproduct'),
    
    path('Adminvieworder_Details',views.Adminvieworder_Details,name='Adminvieworder_Details'),
    path('dashboard',views.adminDashboard,name='AdminDashboard'),

    path('order_Cancelled/<int:id>',views.order_Cancelled,name='order_Cancelled'),
    path('order_Shipped/<int:id>',views.order_Shipped,name='order_Shipped'),
    path('order_Out_For_delivery/<int:id>',views.order_Out_For_delivery,name='order_Out_For_delivery'),
    path('order_Delivered/<int:id>',views.order_Delivered,name='order_Delivered'),
    
    #------------------------- sales report ------------------------ #

    path("salesreport",views.salesreport,name="salesreport"),
    path("monthly_report/<int:date>/",views.monthly_report,name="monthly_report"),
    path("yearly_report/<int:date>/",views.yearly_report,name="yearly_report"),
    path("date_range",views.date_range,name="date_range"),
    
    
    #------------------------- coupon management ------------------------ #
    path("view_coupon",views.view_coupon,name="view_coupon"),
    path("add_coupon",views.add_coupon,name="add_coupon"),
    path("block_coupon/<int:id>/", views.block_coupon,name="block_coupon"),
    path("delete_coupon/<int:id>/",views.delete_coupon,name="delete_coupon"),
    
    #------------------------- category offer management ------------------------ #
    path("newcategoryoffer",views.New_CategoryOffer,name="NewCategoryOffer"),
    path("categoryoffers",views.View_CategoryOffers,name="ViewCategoryOffer"),
    path("editcategoryoffers/<int:id>/",views.Edit_CategoryOffer,name="EditCategoryOffer"),
    path("blockcategoryoffers/<int:id>/",views.Block_CategoryOffer,name="BlockCategoryOffer"),
    path("unblockcategoryoffers/<int:id>/",views.UnBlock_CategoryOffer,name="UnBlockCategoryOffer"),
    path("deletecategoryoffers/<int:id>/",views.Delete_CategoryOffer,name="DeleteCategoryOffer"),


#------------------------- Product offer management ------------------------ #
    path("newproductoffer",views.New_ProductOffer,name="NewProductOffer"),
    path("productoffers",views.View_ProductOffers,name="ViewProductOffer"),
    path("editproductoffers/<int:id>/",views.Edit_ProductOffer,name="EditProductOffer"),
    path("blockproductoffers/<int:id>/",views.Block_ProductOffer,name="BlockProductOffer"),
    path("unblockproductoffers/<int:id>/",views.UnBlock_ProductOffer,name="UnBlockProductOffer"),
    path("deleteproductoffers/<int:id>/",views.Delete_ProductOffer,name="DeleteProductOffer"),


] 


