import random
from email.policy import default

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Max, Case, F, FloatField, Q, When
from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
    queryset = Item.objects.exclude(name='Banner').order_by('pk')
    serializer_class = ItemSerializer
    filterset_class = ItemFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    ordering_fields = ['is_sale', 'price']


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
        ids = Item.objects.exclude(name='Banner').values_list('id', flat=True)
        random_ids = random.sample(list(ids), min(len(ids), 5))
        return Item.objects.filter(id__in=random_ids)


class SliderAPIView(ListAPIView):
    serializer_class = SliderSerializer

    def get_queryset(self):
        # Get banner item (assuming there's only one)
        banner_item = Item.objects.filter(name='Banner')

        # Get all item IDs excluding the banner
        all_ids = Item.objects.exclude(name='Banner').values_list('id', flat=True)

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
        items = Item.objects.exclude(name='Banner').filter(is_sale=True, sub_category_id=sub_category_id).order_by('id')
        items_data = ItemSerializer(items, many=True).data
        return Response({
            'items': items_data,
        })


class APISettingsAPIView(APIView):
    def get(self, request):
        price_range = Item.objects.exclude(name='Banner').aggregate(
            min_price=Min(
                Case(
                    When(is_sale=True, then=F('sale_price')),
                    default=F('price'),
                    output_field=FloatField()

                )
            ),
            max_price=Max(
                Case(
                    When(is_sale=True, then=F('sale_price')),
                    default=F('price'),
                    output_field=FloatField()
                )
            )
        )
        sub_categories = SubCategory.objects.filter(items__isnull=False).distinct()
        colors = Color.objects.filter(items__isnull=False).distinct()
        banner_item = Item.objects.filter(name='Banner').first()

        return Response({
            'price_range': price_range,
            'sub_categories': SubCategorySerializer(sub_categories, many=True).data,
            'colors': ColorSerializer(colors, many=True).data,
            'banner_item': ItemSerializer(banner_item).data
        })


class SearchAPIView(APIView):

    def post(self, request):
        q = request.data.get('search_query')
        sub_category_id = request.data.get('sub_category_id')
        color_id = request.data.get('color_id')
        min_price = request.data.get('min_price')
        max_price = request.data.get('max_price')

        items = Item.objects.all()

        if q:
            items = items.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            )

        if sub_category_id:
            items = items.filter(sub_category_id=sub_category_id)

        if color_id:
            items = items.filter(color_id=color_id)

        # Add temp effective_price
        items = items.annotate(
            effective_price=Case(
                When(is_sale=True, then=F('sale_price')),
                default=F('price'),
                output_field=FloatField()
            )
        )

        if min_price is not None:
            items = items.filter(effective_price__gte=min_price)

        if max_price is not None:
            items = items.filter(effective_price__lte=max_price)

        serialized_items = ItemSerializer(items, many=True).data

        return Response({
            'items': serialized_items,
            'count': len(serialized_items)
        }, status=status.HTTP_200_OK)
