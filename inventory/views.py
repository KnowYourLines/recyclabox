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
        queryset = self.get_queryset().filter(quantity__gt=0)
        result = self.get_serializer(queryset, many=True)
        return Response(result.data)

    @action(detail=False, methods=["get"])
    def sold_out(self, request):
        queryset = self.get_queryset().filter(quantity=0)
        result = self.get_serializer(queryset, many=True)
        return Response(result.data)

    @action(detail=True, methods=["patch"])
    def quantity(self, request, **kwargs):
        instance = self.get_object()
        query_params = QueryParamSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)
        existing = model_to_dict(instance)
        product = self.get_serializer(
            instance,
            data={
                "quantity": existing["quantity"] + query_params.validated_data["change"]
            },
            partial=True,
        )
        product.is_valid(raise_exception=True)
        product.save()
        return Response(product.validated_data)
