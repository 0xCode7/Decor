import django_filters
from .models import Item
from rest_framework import filters


class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='contains')
    color = django_filters.CharFilter(field_name='color', lookup_expr='contains')

    class Meta:
        model = Item
        fields = []
