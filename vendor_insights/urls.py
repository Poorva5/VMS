from django.urls import include, path
from rest_framework import routers
from .views import VendorView, PurchaseOrderView

router = routers.DefaultRouter()
router.register(r"vendors", VendorView, basename="vendor_api")

po_router = routers.DefaultRouter()
po_router.register(r"", PurchaseOrderView, basename="purchase_order_api")

urlpatterns = [
    path("", include(router.urls)),
    path("purchase_orders/", include(po_router.urls)),
]
