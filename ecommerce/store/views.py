from django.shortcuts import render
from .models import Product,Order
# Create your views here.
def main(request):
    context = {}
    return render(request,'main.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order ,created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.itemorder_set.all()
    else:
        items = []
        order = {'totalPrice':0,'totalItems':0}
    context = {'order':order,'items':items}
    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
            customer = request.user.customer
            order ,created = Order.objects.get_or_create(customer = customer,complete = False)
            items = order.itemorder_set.all()
    else:
            items = []
            order = {'totalPrice':0,'totalItems':0}
    context = {'order':order,'items':items}    
    return render(request,'checkout.html',context)

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request,'store.html',context)