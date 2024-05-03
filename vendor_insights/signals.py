from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder, HistoricalPerformance


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    if instance.status == "Completed" and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_orders = vendor.purchase_orders.filter(status="Completed")

        on_time_orders = completed_orders.filter(
            delivery_date__lte=instance.delivery_date
        )
        on_time_delivery_rate = (
            on_time_orders.count() / completed_orders.count()
        ) * 100

        quality_ratings = completed_orders.exclude(quality_rating__isnull=True)
        total_quality_rating = sum(
            quality_ratings.values_list("quality_rating", flat=True)
        )
        total_completed_orders = completed_orders.count()

        if total_completed_orders > 0:
            quality_rating_avg = total_quality_rating / total_completed_orders
        else:
            quality_rating_avg = 0

        ack_orders = completed_orders.exclude(acknowledgment_date__isnull=True)
        total_ack_time = sum(
            (order.acknowledgment_date - order.issue_date).total_seconds()
            for order in ack_orders
        )
        average_response_time = (
            total_ack_time / ack_orders.count() if ack_orders.count() > 0 else 0
        )

        average_response_time_hrs = average_response_time / 3600

        fulfilled_orders = completed_orders.exclude(status="Completed with issues")
        fulfillment_rate = (
            fulfilled_orders.count() / vendor.purchase_orders.count()
        ) * 100

        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            date=instance.delivery_date,
            defaults={
                "on_time_delivery_rate": on_time_delivery_rate,
                "quality_rating_avg": quality_rating_avg,
                "average_response_time": average_response_time_hrs,
                "fulfillment_rate": fulfillment_rate,
            },
        )
