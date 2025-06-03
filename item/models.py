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
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Sub Categories'


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField()
    is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
