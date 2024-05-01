from django.shortcuts import render
from .serializers import (
    VendorSerializer,
    PurchaseOrderSerializer,
    HistoricalPerformanceSerializer,
)
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework import viewsets


class VendorView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
