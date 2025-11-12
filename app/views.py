from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from django.http import JsonResponse
from .forms import ProductModelForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def index(request,category_id = None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(id = category_id)
    else:
        products = Product.objects.all()

    context = {
        'categories' : categories,
        'products' : products
    }
    return render(request,'app/home.html',context)



def detail(request,product_id):
    product = Product.objects.get(id = product_id)
    if not product:
        return  JsonResponse(data={'message':'Oops. Page Not Found','status_code':404})
    
    context = {
        'product': product_id
    }

    return render (request,'app/detail.html',context)
    

@login_required(login_url='/admin/')
def create_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Product successfully created "
            )

            
            return redirect('app:create')
    else:
        form = ProductModelForm()
        
                
    context = {
        'form':form
    }
    return render(request,'app/create.html',context)


def delete_product(request,pk):
    product = Product.objects.get(id = pk)
    if product:
        product.delete()
        return redirect('app:index')    
    
    return render(request,'app/detail.html')



def update(request, category_idd):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    category = get_object_or_404(Category, id=category_idd)

    form = ProductModelForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST":
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
            return redirect('product_detail', product.id)

    context = {
        'form': form,
        'product': product,
        'category': category
    }
    return render(request, 'update.html', context)
