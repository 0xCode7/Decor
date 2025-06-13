import random
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Max
from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from item.models import Category, Item, SubCategory, Color
from item.serializers import (CategorySerializer, ItemSerializer,
                              SliderSerializer, SubCategorySerializer, ColorSerializer)
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

    def get_search_fields(self, view, request):
        return [field.name for field in self.get_serializer().Meta.model._meta.fields
                if isinstance(field, (models.CharField, models.TextField))]

    ordering_fields = ['is_sale', 'price']
    ordering = ['is_sale']


class NewItemsViewSet(ListAPIView):
    queryset = Item.objects.order_by('-id')[:3]
    serializer_class = ItemSerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        queryset = SubCategory.objects.order_by('id')
        main_category_id = self.request.query_params.get('main_category_id')
        if main_category_id:
            queryset = queryset.filter(main_category_id=main_category_id)
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


class SpecialOfferAPIView(APIView):
    serializer_class = ItemSerializer

    def get(self, request):
        sub_category_id = request.query_params.get('sub_category_id')

        # All Sub Category With Special Offers
        sub_categories = SubCategory.objects.filter(items__is_sale=True).distinct()
        sub_categories_data = SubCategorySerializer(sub_categories, many=True).data

        if not sub_category_id:
            return Response({
                'sub-categories': sub_categories_data
            })
        items = Item.objects.filter(is_sale=True, sub_category_id=sub_category_id).order_by('id')
        items_data = ItemSerializer(items, many=True).data
        return Response({
            'items': items_data,
            'sub-categories': sub_categories_data,

        })


class SearchOptionsAPIView(APIView):
    def get(self, request):
        price_range = Item.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
        sub_categories = SubCategory.objects.filter(items__isnull=False).distinct()
        colors = Color.objects.filter(items__isnull=False).distinct()

        return Response({
            'price_range': price_range,
            'sub_categories': SubCategorySerializer(sub_categories, many=True).data,
            'colors': ColorSerializer(colors, many=True).data
        })
