from utils.test_utils import APITest
from vendor_insights.models import Vendor, PurchaseOrder
from vendor_insights.factory import VendorFactory, UserFactory, PurchaseOrderFactory
from django.urls import reverse
from urllib import response
from rest_framework import status
from datetime import datetime
from django.utils import timezone

import logging

logger = logging.getLogger(__name__)


class VendorTestCase(APITest):
    """
    Test: Vendor CRUD APIs
    This test covers the endpoints for the Vendor APIs
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.user = UserFactory(username="George")
        self.series = VendorFactory()

    def test_get_vendors(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        response = self.client.get(reverse("vendor_insights:vendor-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        vendor_instance = VendorFactory.build()
        vendor_data = {
            "name": vendor_instance.name,
            "contact_details": vendor_instance.contact_details,
            "address": vendor_instance.address,
            "vendor_code": vendor_instance.vendor_code,
            "on_time_delivery_rate": vendor_instance.on_time_delivery_rate,
            "quality_rating_avg": vendor_instance.quality_rating_avg,
            "average_response_time": vendor_instance.average_response_time,
            "fulfillment_rate": vendor_instance.fulfillment_rate,
        }
        response = self.client.post(
            reverse("vendor_insights:vendor-list"), data=vendor_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_vendor(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        vendor_instance = VendorFactory()
        updated_data = {
            "name": "Updated Vendor Name",
            "vendor_code": "POO098",
            "contact_details": "Updated Contact Details",
            "address": "Updated Address",
            "on_time_delivery_rate": 90.0,
            "quality_rating_avg": 4.0,
            "average_response_time": 3.0,
            "fulfillment_rate": 95.0,
        }
        response = self.client.put(
            reverse("vendor_insights:vendor-detail", kwargs={"pk": vendor_instance.id}),
            data=updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vendor(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        vendor_instance = VendorFactory()
        response = self.client.get(
            reverse("vendor_insights:vendor-detail", kwargs={"pk": vendor_instance.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vendor(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        vendor_instance = VendorFactory()
        response = self.client.delete(
            reverse("vendor_insights:vendor-detail", kwargs={"pk": vendor_instance.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PurchaseOrderTestCase(APITest):
    """
    Test: Purchase Order CRUD APIs
    This test covers the endpoints for the Purchase Order APIs
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.user = UserFactory(username="George")
        self.series = PurchaseOrderFactory()

    def test_get_purchase_orders(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        response = self.client.get(reverse("vendor_insights:po-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        po_instance = PurchaseOrderFactory.build()
        vendor_instance = VendorFactory()
        po_data = {
            "po_number": po_instance.po_number,
            "vendor": {
                "id": vendor_instance.id,
                "name": vendor_instance.name,
                "contact_details": vendor_instance.contact_details,
                "address": vendor_instance.address,
                "vendor_code": vendor_instance.vendor_code,
                "on_time_delivery_rate": vendor_instance.on_time_delivery_rate,
                "quality_rating_avg": vendor_instance.quality_rating_avg,
                "average_response_time": vendor_instance.average_response_time,
                "fulfillment_rate": vendor_instance.fulfillment_rate,
            },
            "order_date": po_instance.order_date,
            "delivery_date": po_instance.delivery_date,
            "items": po_instance.items,
            "quantity": po_instance.quantity,
            "status": po_instance.status,
            "quality_rating": po_instance.quality_rating,
            "issue_date": po_instance.issue_date,
            "acknowledgment_date": po_instance.acknowledgment_date,
        }
        response = self.client.post(
            reverse("vendor_insights:po-list"), data=po_data, format="json"
        )
        if response.status_code != status.HTTP_201_CREATED:
            logger.error("Error updating po: %s", response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_purchase_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        po_instance = PurchaseOrderFactory()
        current_time = datetime.now(tz=timezone.utc).isoformat()
        updated_po_data = {
            "po_number": po_instance.po_number,
            "vendor": {
                "name": "Updated Vendor Name",
                "vendor_code": "POO098",
                "contact_details": "Updated Contact Details",
                "address": "Updated Address",
                "on_time_delivery_rate": 90.0,
                "quality_rating_avg": 4.0,
                "average_response_time": 3.0,
                "fulfillment_rate": 95.0,
            },
            "order_date": current_time,
            "delivery_date": current_time,
            "items": [{"item_name": "Laptop"}],
            "quantity": 20,
            "status": "Completed",
            "quality_rating": 4.5,
            "issue_date": current_time,
            "acknowledgment_date": current_time,
        }
        response = self.client.put(
            reverse("vendor_insights:po-detail", kwargs={"pk": po_instance.id}),
            data=updated_po_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_purchase_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        po_instance = PurchaseOrderFactory()
        response = self.client.get(
            reverse("vendor_insights:po-detail", kwargs={"pk": po_instance.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(self.user))
        po_instance = PurchaseOrderFactory()
        response = self.client.delete(
            reverse("vendor_insights:po-detail", kwargs={"pk": po_instance.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
