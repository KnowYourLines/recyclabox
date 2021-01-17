from http import HTTPStatus

from rest_framework.test import APISimpleTestCase


class ProductIntegrationTest(APISimpleTestCase):
    databases = {"default"}

    def test_register_a_product(self):
        new_product = {
            "sku": "2346",
            "name": "Apple iPhone 5",
            "quantity": 5,
            "price": 59.99,
        }
        response = self.client.post("/inventory/", new_product, format="json")
        assert response.status_code == HTTPStatus.CREATED
