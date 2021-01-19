import datetime
from http import HTTPStatus

from django.test import TransactionTestCase

from inventory.models import Product


class ProductIntegrationTest(TransactionTestCase):
    def test_register_a_product(self):
        new_product = {
            "sku": "2346",
            "name": "Apple iPhone 5",
            "quantity": 5,
            "price": 59.99,
        }
        response = self.client.post("/inventory/", new_product, format="json")
        assert response.status_code == HTTPStatus.CREATED
        assert response.data == {
            "sku": "2346",
            "name": "Apple iPhone 5",
            "quantity": 5,
            "price": 59.99,
        }

    def test_retrieve_product_by_sku(self):
        salt = (
            datetime.datetime.now()
            .isoformat()
            .replace(":", "")
            .replace("-", "")
            .replace(".", "")
        )
        created_product = Product(sku=salt, name="world", quantity=5, price=59.99)
        created_product.save()
        response = self.client.get(f"/inventory/{salt}/")
        assert response.status_code == HTTPStatus.OK
        assert response.data == {
            "sku": salt,
            "name": "world",
            "quantity": 5,
            "price": 59.99,
        }

    def test_retrieves_all_available_products(self):
        salt = (
            datetime.datetime.now()
            .isoformat()
            .replace(":", "")
            .replace("-", "")
            .replace(".", "")
        )
        created_product = Product(sku=salt, name="world", quantity=5, price=59.99)
        created_product.save()
        created_product = Product(
            sku="hello" + salt, name="world", quantity=5, price=59.99
        )
        created_product.save()
        created_product = Product(
            sku="goodbye" + salt, name="world", quantity=0, price=59.99
        )
        created_product.save()
        response = self.client.get("/inventory/available/")
        assert response.status_code == HTTPStatus.OK
        assert response.data == [
            {"name": "world", "quantity": 5, "price": 59.99, "sku": salt},
            {"name": "world", "quantity": 5, "price": 59.99, "sku": "hello" + salt},
        ]

    def test_retrieves_all_sold_out_products(self):
        salt = (
            datetime.datetime.now()
            .isoformat()
            .replace(":", "")
            .replace("-", "")
            .replace(".", "")
        )
        created_product = Product(sku=salt, name="world", quantity=5, price=59.99)
        created_product.save()
        created_product = Product(
            sku="hello" + salt, name="world", quantity=5, price=59.99
        )
        created_product.save()
        created_product = Product(
            sku="goodbye" + salt, name="world", quantity=0, price=59.99
        )
        created_product.save()
        response = self.client.get("/inventory/sold_out/")
        assert response.status_code == HTTPStatus.OK
        assert response.data == [
            {"name": "world", "quantity": 0, "price": 59.99, "sku": "goodbye" + salt},
        ]

    def test_update_product_quantity_by_value_change(self):
        created_product = Product(sku="2346", name="world", quantity=5, price=59.99)
        created_product.save()
        response = self.client.patch("/inventory/2346/quantity/?change=-2")
        assert response.status_code == HTTPStatus.OK
        response = self.client.get("/inventory/2346/")
        assert response.data == {
            "sku": "2346",
            "name": "world",
            "quantity": 3,
            "price": 59.99,
        }
        response = self.client.patch("/inventory/2346/quantity/?change=5")
        assert response.status_code == HTTPStatus.OK
        response = self.client.get("/inventory/2346/")
        assert response.data == {
            "sku": "2346",
            "name": "world",
            "quantity": 8,
            "price": 59.99,
        }
