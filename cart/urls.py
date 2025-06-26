# item/urls.py

from django.urls import path
from .views import cart_detail, cart_add, cart_update, cart_delete, cart_clear

urlpatterns = [
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/', cart_add, name='cart_add'),
    path('cart/update/', cart_update, name='cart_update'),
    path('cart/delete/', cart_delete, name='cart_delete'),
    path('cart/clear/', cart_clear, name='cart_clear'),
]
