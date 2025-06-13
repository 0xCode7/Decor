from .models import Item, Category, SubCategory, Color
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    sub_category_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    color = serializers.SlugRelatedField(
        read_only=True,
        slug_field='hex'
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


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'
