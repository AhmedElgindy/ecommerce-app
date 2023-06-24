from django.urls import path
from . import views
urlpatterns = [
    path('',views.main,name="main"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('store/',views.store,name="store"),
]