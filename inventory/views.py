from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from inventory.models import Product
from inventory.serializers import ProductSerializer


class InventoryViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=["get"])
    def available(self, request):
        return Response(self.get_queryset().filter(quantity__gt=0).values())

    @action(detail=False, methods=["get"])
    def sold_out(self, request):
        return Response(self.get_queryset().filter(quantity=0).values())
