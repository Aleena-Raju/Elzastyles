from tokenize import blank_re
from django.db import models

# Create your models here.

import code
from pickle import TRUE
from django.db import models
from category.models import Category
from accounts.models import Account

# Create your models here.


class Product(models.Model):
    product_name        = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=200, unique=True)
    description         = models.TextField(max_length=500, blank=True)
    price               = models.IntegerField()
    image1              = models.ImageField(upload_to='products')
    image2              = models.ImageField(upload_to='products')
    image3              = models.ImageField(upload_to='products')
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add =True)
    modified_date       = models.DateTimeField(auto_now=True)
    discount            = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.product_name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    
    
    
