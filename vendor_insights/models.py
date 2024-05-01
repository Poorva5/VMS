from django.db import models
from utils.models import BaseModel
from django.utils import timezone


class Vendor(BaseModel):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField(null=True, blank=True)
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(
        default=0.0,
        help_text="Tracks the percentage of on-time deliveries.",
    )
    quality_rating_avg = models.FloatField(
        default=0.0,
        help_text="Average rating of quality based on purchase orders",
    )
    average_response_time = models.FloatField(
        default=0.0,
        help_text="Average time taken to acknowledge purchase orders.",
    )
    fulfillment_rate = models.FloatField(
        default=0.0,
        help_text="Percentage of purchase orders fulfilled successfull",
    )

    def __str__(self):
        return self.name


class PurchaseOrder(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    ]
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="purchase_orders"
    )
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    quality_rating = models.FloatField(
        null=True, blank=True, help_text="Rating given to the vendor for this PO"
    )
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the vendor acknowledged the PO.",
    )

    def __str__(self):
        return f"{self.vendor.name} - {self.po_number}"


class HistoricalPerformance(BaseModel):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="historical_performance"
    )
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
