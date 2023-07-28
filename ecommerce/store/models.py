from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.name or str(self.id)
    
class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(null=True,max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True,blank=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url= ''
        
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    date_order = models.DateField(auto_now_add=True,null=True)
    complete = models.BooleanField(default=False,null=True)
    trasaction_id = models.CharField(max_length=200,null=True)


    def __str__(self) -> str:
        return str(self.id)
    #function that calc the total for each item order
    @property
    def totalPrice(self):
        return sum(item.total for item in self.itemorder_set.all())
    
    @property
    def totalItems(self):
        return sum(item.quantity for item in self.itemorder_set.all())
    
    @property
    def shipping(self):
        shipping = False
        for item in self.itemorder_set.all():
            if  not item.product.digital:
                shipping = True
        return shipping


class ItemOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateField(auto_now_add=True,null=True)

    @property
    def total(self) -> int:
        price = self.product.price
        total  = self.quantity * price
        return total

class ShipingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateField(auto_now_add=True,null=True)

    def __str__(self) -> str:
        return self.address




