from django.contrib import admin
from .models import Item, Category, SubCategory, Color


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'sub_category_id')
    list_filter = ['sub_category_id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'main_category_id']


@admin.register(Color)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'hex']
