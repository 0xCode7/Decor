# store/serializers.py

from rest_framework import serializers
from item.models import Item


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.ImageField()
    price = serializers.FloatField()
    sale_price = serializers.FloatField(allow_null=True)
    is_sale = serializers.BooleanField()
    quantity = serializers.IntegerField()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        unit_price = obj.sale_price if obj.is_sale and obj.sale_price else obj.price
        return round(unit_price * obj.quantity, 2)


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.FloatField()
