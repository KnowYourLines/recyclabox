from rest_framework import mixins, viewsets

from inventory.models import Product
from inventory.serializers import ProductSerializer


class InventoryViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
