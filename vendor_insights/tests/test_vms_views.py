from utils.test_utils import APITest
from vendor_insights.models import Vendor, PurchaseOrder
from vendor_insights.factory import VendorFactory, UserFactory
from django.urls import reverse
from urllib import response
from rest_framework import status

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
        if response.status_code != status.HTTP_200_OK:
            logger.error("Error updating venoor: %s", response.content)
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
