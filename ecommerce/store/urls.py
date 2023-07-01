from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.main,name="main"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('store/',views.store,name="store"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

