from django.urls import path
from .views import (
    NewItemsViewSet,
    BestSellerAPIView,
    SliderAPIView,
    SpecialOfferAPIView, SearchOptionsAPIView
)

urlpatterns = [
    path('new/', NewItemsViewSet.as_view(), name='new-collection'),
    path('best-seller/', BestSellerAPIView.as_view(), name='best-seller-list'),
    path('slider/', SliderAPIView.as_view(), name='slider-list'),
    path('offers/', SpecialOfferAPIView.as_view(), name='special-offer'),
    path('search/', SearchOptionsAPIView.as_view(), name='search'),
]
