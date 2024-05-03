from django.test import TestCase
from rest_framework.test import APIClient
import factory
import json
from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {"token": str(refresh.access_token), "refresh": str(refresh)}


class APITest(TestCase):
    """
    Base API Test Case
    """

    def setUp(self):
        """Will setup base for tests"""
        super().setUp()
        self.client = APIClient()

    @staticmethod
    def get_auth_header(user):
        """Get user auth token"""
        token = get_token_for_user(user)["token"]
        return f"Bearer {token}"
