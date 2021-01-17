from http import HTTPStatus

from rest_framework.test import APISimpleTestCase


class ProductIntegrationTest(APISimpleTestCase):
    databases = {"default"}

    def test_register_a_product(self):
        new_product = {
            "SKU": "2345",
            "Name": "Apple iPhone 5",
            "Qty": 5,
            "Price": 59.99,
        }
        response = self.client.create("/product/", new_product, format="json")
        assert response.status_code == HTTPStatus.OK
