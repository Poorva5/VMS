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
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


class VendorView(viewsets.ModelViewSet):
    """
    Viewset to perform CRUD operation on Vendor objects
    """

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        """
        Retrieves Performace metrics for specific Vendor
        """
        try:
            vendor = self.get_object()
            performance_data = HistoricalPerformance.objects.filter(vendor=vendor)
            serializer = HistoricalPerformanceSerializer(performance_data, many=True)
            return Response(serializer.data)
        except HistoricalPerformance.DoesNotExist:
            return Response(
                {"message": "No performance metric present for this vendor"},
                status=status.HTTP_404_NOT_FOUND,
            )


class PurchaseOrderView(viewsets.ModelViewSet):
    """
    viewset to perform CRUD operation on Purchase order objects.
    """

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PurchaseOrderFilter
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Creates new purchase order
        """
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
        """
        Updates purchase order based on provided data
        """
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

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        """
        function to Acknowledge a purchase order
        """
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response(
            {"message": "Purchase order acknowledged successfully"},
            status=status.HTTP_200_OK,
        )
