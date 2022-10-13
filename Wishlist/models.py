from django.db import models
from accounts.models import *
from adminone.models import *
from products.models import *

# Create your models here.
class Wishlist(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    wished_product=models.ForeignKey(Product,on_delete=models.CASCADE)
    added_date=models.DateTimeField(auto_now_add=True)