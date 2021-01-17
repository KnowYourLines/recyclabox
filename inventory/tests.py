from django.test import TestCase

# Create your tests here.
from inventory.serializers import ProductSerializer


class ProductSerializerTest(TestCase):
    def test_serializes_valid_data(self):
        serializer = ProductSerializer(
            data={
                "sku": "2346",
                "name": "Apple iPhone 5",
                "quantity": 5,
                "price": 59.99,
            }
        )
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data == {
            "sku": "2346",
            "name": "Apple iPhone 5",
            "quantity": 5,
            "price": 59.99,
        }
