from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor_code")


admin.site.register(Vendor, VendorAdmin)


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "po_number", "status")


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)


class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "on_time_delivery_rate")


admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)
