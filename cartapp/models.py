from django.db import models
from accounts.models import Account
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from category.models import Category

# Create your models here.

class Cart(models.Model):
    cart_id         = models.CharField(max_length=50,unique=True)
    date_added      = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.cart_id

class Cart_Products(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity        = models.PositiveIntegerField()
    is_active       = models.BooleanField(default=True)


    def __unicode__(self):
        return self.product.product_name

    def sub_total(self):
        return self.product.price * self.quantity


class Address(models.Model):
    user                        = models.ForeignKey(Account, on_delete=models.CASCADE)
    Buyername                   = models.CharField(max_length=50)
    phone_number                = models.CharField(max_length=25)
    email                       = models.EmailField(max_length=50, null=True)
    Buyers_Address              = models.CharField(max_length=100)      
    pincode                     = models.IntegerField(null=True)
    city                        = models.CharField( max_length=20)
    state                       = models.CharField( max_length=100,default='Kerala')
    country                     = models.CharField( max_length=20,default='India')

    def __str__(self):
        return self.user.username
    
    
    
    
    
    
    
    
    

# class Categoryoffer(models.Model):
#     category= models.OneToOneField(Category, related_name='category_offers', on_delete=models.CASCADE)
#     discount= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
#     is_active = models.BooleanField(default=True)


#     def __str__(self):   
#         return self.category.title    

# class SubCategoryoffer(models.Model):
#     subcategory= models.OneToOneField(SubCategories, related_name='subcategory_offers', on_delete=models.CASCADE)
#     discount= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
#     is_active = models.BooleanField(default=True)


    # def __str__(self):   
    #  return self.subcategory.title     

# class Productoffer(models.Model):
#     product= models.OneToOneField(Product, related_name='subcategory_category_offers', on_delete=models.CASCADE)
#     discount= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
#     is_active = models.BooleanField(default=True)


#     def __str__(self):   
#         return self.product.product_name 

# class Coupons(models.Model):
#     coupon_code=models.CharField(max_length=100)
#     description=models.CharField(max_length=100,null=True)
#     valid_from=models.DateField(auto_now=True)
#     valid_to=models.DateField(null=True)
#     discount=models.IntegerField(null=True)
#     is_active=models.BooleanField(default=True)
#     min_amount=models.IntegerField(null=True)
#     max_amount=models.IntegerField(null=True)

# class CouponUsedUsers(models.Model):
#     user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
#     coupon=models.ForeignKey(Coupons,on_delete=models.CASCADE,null=True)
#     status=models.BooleanField(default=False)

