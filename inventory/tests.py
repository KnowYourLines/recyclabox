from django.test import TestCase

# Create your tests here.
from inventory.serializers import ProductSerializer, QueryParamSerializer


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

    def test_fails_if_data_invalid(self):
        serializer = ProductSerializer(
            data={
                "sku": "2346",
                "quantity": 5,
                "price": 59.99,
            }
        )
        assert not serializer.is_valid()


class QueryParamSerializerTest(TestCase):
    def test_serializes_valid_data(self):
        serializer = QueryParamSerializer(data={"change": 5})
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data == {"change": 5}

    def test_fails_if_data_invalid(self):
        serializer = QueryParamSerializer(data={"change": "abc"})
        assert not serializer.is_valid()
