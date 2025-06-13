from django.urls import path
from .views import (
    NewItemsViewSet,
    BestSellerAPIView,
    SliderAPIView,
    SpecialOfferAPIView, SearchAPIView, APISettingsAPIView
)

urlpatterns = [
    path('new/', NewItemsViewSet.as_view(), name='new-collection'),
    path('best-seller/', BestSellerAPIView.as_view(), name='best-seller-list'),
    path('slider/', SliderAPIView.as_view(), name='slider-list'),
    path('offers/', SpecialOfferAPIView.as_view(), name='special-offer'),
    path('api-settings/', APISettingsAPIView.as_view(), name='api-settings'),
    path('search/', SearchAPIView.as_view(), name='search'),
]
