from django.urls import include, path
from rest_framework import routers
from .views import VendorView, PurchaseOrderView

app_name = "vendor_insights"

router = routers.DefaultRouter()
router.register(r"vendors", VendorView, basename="vendor")

po_router = routers.DefaultRouter()
po_router.register(r"", PurchaseOrderView, basename="po")

urlpatterns = [
    path("", include(router.urls)),
    path("purchase_orders/", include(po_router.urls)),
]
