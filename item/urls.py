from django.urls import path
from .views import (
    NewItemsViewSet,
    BestSellerAPIView,
    SliderAPIView,
    SpecialOfferCategoriesAPIView,
    SpecialOfferItemsAPIView
)

urlpatterns = [
    path('new/', NewItemsViewSet.as_view(), name='new-collection'),
    path('best-seller/', BestSellerAPIView.as_view(), name='best-seller-list'),
    path('slider/', SliderAPIView.as_view(), name='slider-list'),
    path('offers/', SpecialOfferCategoriesAPIView.as_view(), name='special-offer'),
    path('offers/<int:sub_category_id>', SpecialOfferItemsAPIView.as_view(), name='special-offer')
]
