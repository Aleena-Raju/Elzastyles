from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signin',views.signin,name='register'),
    path('signup',views.signup,name='signup'),
    path('logout',views.signout,name='logout'),
    path('loginotp/<int:id>/',views.loginotp,name='loginOtp'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('invoice/<int:id>',views.invoice,name='invoice'),

]