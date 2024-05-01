from django.urls import include, path
from rest_framework import routers
from .views import VendorView

router = routers.DefaultRouter()
router.register(r"", VendorView, basename="vendor_api")

urlpatterns = [
    path("", include(router.urls)),
]
