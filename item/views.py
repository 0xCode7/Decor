# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from item.models import Category, Item, SubCategory
from item.serailizers import ItemSerializer, CategorySerializer, SubCategorySerializer


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
