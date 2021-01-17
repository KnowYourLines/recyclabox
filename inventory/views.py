from django.forms import model_to_dict
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from inventory.models import Product
from inventory.serializers import ProductSerializer, QueryParamSerializer


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

    @action(detail=True, methods=["patch"])
    def quantity(self, request, **kwargs):
        instance = self.get_object()
        serializer = QueryParamSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        existing = model_to_dict(instance)
        serializer = self.get_serializer(
            instance,
            data={
                "quantity": existing["quantity"] + serializer.validated_data["change"]
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)
