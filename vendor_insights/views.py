from django.shortcuts import render
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    HistoricalPerformanceSerializer,
)
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .filters import PurchaseOrderFilter
from django_filters import rest_framework as filters
from rest_framework.decorators import action


class VendorView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        performance_data = HistoricalPerformance.objects.filter(vendor=vendor)
        serializer = HistoricalPerformanceSerializer(performance_data, many=True)
        return Response(serializer.data)


class PurchaseOrderView(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PurchaseOrderFilter

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            vendor_data = data.get("vendor")
            vendor_instance, _ = Vendor.objects.get_or_create(
                id=vendor_data.get("id"), defaults=vendor_data
            )
            serializer.validated_data.pop("vendor", None)

            purchase_order_instance = serializer.save(vendor=vendor_instance)
            purchase_order_serializer = PurchaseOrderSerializer(purchase_order_instance)

            return Response(
                purchase_order_serializer.data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = request.data
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)

            vendor_data = data.get("vendor")
            if vendor_data:
                vendor_instance, _ = Vendor.objects.get_or_create(
                    id=vendor_data.get("id"), defaults=vendor_data
                )
                serializer.validated_data.pop("vendor", None)
                serializer.validated_data["vendor"] = vendor_instance

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
