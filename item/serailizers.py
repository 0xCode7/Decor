from .models import Item, Category, SubCategory
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Item
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'image']
