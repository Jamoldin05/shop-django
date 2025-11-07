from django.shortcuts import render
from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories' : categories,
        'products' : products
    }
    return render(request,'app/home.html',context)


