from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store, name='products_by_category'),
    path('<int:id>/',views.product_detail, name='single_product_detail'),
    path('search/',views.search, name='search'),
]