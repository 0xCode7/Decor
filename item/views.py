import random
from django.db.models import Max
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from item.models import Category, Item, SubCategory
from item.serailizers import ItemSerializer, CategorySerializer, SubCategorySerializer, SliderSerializer


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all().order_by('id')
    serializer_class = SubCategorySerializer


class BestSellerAPIView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        ids = Item.objects.values_list('id', flat=True)
        random_ids = random.sample(list(ids), min(len(ids), 5))
        return Item.objects.filter(id__in=random_ids)


class SliderAPIView(ListAPIView):
    serializer_class = SliderSerializer

    def get_queryset(self):
        ids = Item.objects.values_list('id', flat=True)
        random_ids = random.sample(list(ids), min(len(ids), 3))
        return Item.objects.filter(id__in=random_ids)