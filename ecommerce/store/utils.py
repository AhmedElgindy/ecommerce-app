import json
from .models import Product,Order,Customer,ItemOrder
def cookieCart(request):
    try:
            cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print("CART:",cart)
    print(cart)
    order = {'totalPrice':0,'totalItems':0,'shipping':False}

    items = []
    for i in cart:
        try:
            proudct = Product.objects.get(id = i )
            total = (proudct.price)* cart[i]['quantity']
            order['totalPrice'] += total
            order['totalItems'] += cart[i]['quantity']
            item = {"product":{"id":proudct.id,"price":proudct.price,"name":proudct.name,"imageURL":proudct.imageURL},"quantity":cart[i]['quantity'],"total":total}
            items.append(item)

            if(proudct.digital == False):
                order['shipping'] = True
        except:
                pass
    
    cartItem = order['totalItems']

    return {'order':order,'items':items,"cartItem":cartItem}

def cookieData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order ,created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.itemorder_set.all()
        cartItem = order.totalItems
    else:
        cookiedata = cookieCart(request)
        order = cookiedata['order']
        items = cookiedata['items']
        cartItem = cookiedata['cartItem']
    return {'order':order,'items':items,"cartItem":cartItem}

def guestOrder(request,data):
    email = data['form']['email']
    name = data['form']['name']
    cookiedata = cookieCart(request)
    items = cookiedata['items']

    customer,created = Customer.objects.get_or_create(
        email = email
    )
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer = customer,
        complete = False
    )
    for item in items:
        product = Product.objects.get(id = item['product']['id'])
        itemorder = ItemOrder.objects.create(
            product = product,
            order = order ,
            quantity = item['quantity']
        )
    return customer,order