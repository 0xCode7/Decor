from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icons', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    main_category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='icons', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Sub Categories'


# models.py
class Color(models.Model):
    name = models.CharField(max_length=50, default='Red')
    hex = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField()
    is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField(blank=True, null=True)
    color = models.ForeignKey('Color', on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    sub_category_id = models.ForeignKey('SubCategory', on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='items')
    rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
