import random
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Max
from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from item.models import Category, Item, SubCategory
from item.serializers import (CategorySerializer, ItemSerializer,
                              SliderSerializer, SubCategorySerializer)
from .filters import ItemFilter
from itertools import chain

def get_filter_backends(self):
    fb = super().get_filter_backends()
    print("filter_backends type:", type(fb), fb)
    return fb


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.order_by('pk')
    serializer_class = ItemSerializer
    filterset_class = ItemFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['is_sale', 'price']
    ordering = ['is_sale']


class NewItemsViewSet(ListAPIView):
    queryset = Item.objects.order_by('-id')[:3]
    serializer_class = ItemSerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        queryset = SubCategory.objects.order_by('id')
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(main_category_id=category_id)
        return queryset


class BestSellerAPIView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        ids = Item.objects.values_list('id', flat=True)
        random_ids = random.sample(list(ids), min(len(ids), 5))
        return Item.objects.filter(id__in=random_ids)


class SliderAPIView(ListAPIView):
    serializer_class = SliderSerializer

    def get_queryset(self):
        # Get banner item (assuming there's only one)
        banner_item = Item.objects.filter(name='banner discount slider')

        # Get all item IDs excluding the banner
        all_ids = Item.objects.exclude(name='banner discount slider').values_list('id', flat=True)

        # Get up to 3 random items excluding banner
        random_ids = random.sample(list(all_ids), min(len(all_ids), 3))
        random_items = Item.objects.filter(id__in=random_ids)

        # Combine banner first, then random items
        return list(chain(banner_item, random_items))


class SpecialOfferCategoriesAPIView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        items = Item.objects.filter(is_sale=True).order_by('id')

        category_name = self.request.query_params.get('category')
        if category_name:
            items = items.filter(category__name__iexact=category_name)

        return items

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        subcategories = SubCategory.objects.filter(items__is_sale=True).distinct()
        categories_data = SubCategorySerializer(subcategories, many=True).data

        return Response({
            'sub-categories': categories_data,
        })


class SpecialOfferItemsAPIView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        sub_category_id = self.kwargs.get('sub_category_id')
        items = Item.objects.filter(is_sale=True)

        if sub_category_id:
            items = items.filter(category__id=sub_category_id)

        return items
