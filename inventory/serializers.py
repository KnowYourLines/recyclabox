from rest_framework import serializers

from inventory.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "quantity", "price", "sku"]


class QueryParamSerializer(serializers.Serializer):
    change = serializers.IntegerField()
