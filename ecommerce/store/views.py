from django.shortcuts import render
from .models import Product,Order,ItemOrder,ShipingAddress,Customer
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

from .utils import cookieData,guestOrder
def main(request):
    context = {}
    return render(request,'main.html',context)

# check if the user is auth then getting th order 
# then getting the items in that order and pass it to the context 
#! using DRY for all 3 views 
def cart(request):
    cookiedata = cookieData(request)
    order = cookiedata['order']
    items = cookiedata['items']
    cartItem = cookiedata['cartItem']
        
    context = {'order':order,'items':items,"cartItem":cartItem}
    return render(request,'cart.html',context)

# * the same as main
def checkout(request):
    cookiedata = cookieData(request)
    order = cookiedata['order']
    items = cookiedata['items']
    cartItem = cookiedata['cartItem']

    context = {'order':order,'items':items,"cartItem":cartItem}    
    return render(request,'checkout.html',context)

# * getting the all product to present in the store page 

def store(request):
    cookiedata = cookieData(request)
    cartItem = cookiedata['cartItem']

    products = Product.objects.all()
    context = {'products': products,"cartItem":cartItem}

    return render(request,'store.html',context)

@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data.get('productId')
    action = data.get('action')
    print(productId)
    print(action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = ItemOrder.objects.get_or_create(order=order, product=product)

    if action == "add":
        if orderItem.quantity is not None:
            orderItem.quantity += 1
        else:
            orderItem.quantity = 1
    elif action == "remove":
        if orderItem.quantity is not None:
            orderItem.quantity -= 1
        else:
            orderItem.quantity = 0

    if orderItem.quantity <= 0:
        orderItem.delete()
    else:
        orderItem.save()

    return JsonResponse({'message': 'Data received successfully'}, status=200)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
    else:
        customer,order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.trasaction_id = transaction_id

    if total == float(order.totalPrice):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShipingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']

        )

    return JsonResponse("hello",safe=False)