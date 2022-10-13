from email.policy import default
from itertools import product
from django.db import models
from accounts.models import Account
from products.models import Product 
from category.models import Category
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length= 50,null=True)
    discount_percentage    = models.IntegerField(null=True)
    is_active   = models.BooleanField(default=True)
    
    def __str__(self):
        return self.coupon_code
    
class UsedCoupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username
    
    
    
class Productoffer(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discount = models.IntegerField(validators = [MinValueValidator(0) , MaxValueValidator(99)], null=True, default = 0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.product.product_name
    
    
class Categoryoffer(models.Model):
    category  = models.OneToOneField(Category, on_delete=models.CASCADE)
    discount = models.IntegerField(validators = [MinValueValidator(0) , MaxValueValidator(99)], null=True, default = 0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.category.category_name
    