from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.FloatField()
    sku = models.SlugField(max_length=255, unique=True)
