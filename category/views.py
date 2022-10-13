from django.shortcuts import render
from extra.models import OfferCategory
from nastylesstore.category.models import Category
from nastylesstore.extra.models import Categoryoffer
from products.models import Product
# Create your views here.
def categoryOfffer(request, id):
    category = Category.objects.all()
    products = Product.objects.filter(category_id= id)
    for r in products:
        try:
            Coffer = Categoryoffer.objects.get(category = r.category)
            cat    = Coffer.discount
            if Coffer:
                r.discount = int(r.price - (r.price*(cat/100)))
                r.save()
            if not Coffer:
                r.discount = None
                r.save()
        except:
            r.discount = None
            r.save()
        context = {
            'products':products,
            'category':category,
        }
        return render(request, 'View_CategoryOffer.html',context)