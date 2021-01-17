from rest_framework import serializers

from inventory.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "quantity", "price", "sku"]
