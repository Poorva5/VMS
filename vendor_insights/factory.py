from utils.utility import CoreUtil
import factory
from .models import Vendor, PurchaseOrder
from user.models import User
from django.utils import timezone
from datetime import datetime


def generate_code():
    return CoreUtil.get_short_code()


class VendorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vendor

    name = factory.Faker("company")
    contact_details = factory.Faker("phone_number")
    address = factory.Faker("address")
    vendor_code = factory.Sequence(lambda n: generate_code())
    on_time_delivery_rate = factory.Faker("pyfloat", max_value=100)
    quality_rating_avg = factory.Faker("pyfloat", max_value=5)
    average_response_time = factory.Faker("pyfloat", min_value=0)
    fulfillment_rate = factory.Faker("pyfloat", max_value=100)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Faker("email")
    password = factory.Faker("password")


class PurchaseOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrder

    po_number = factory.Sequence(lambda n: generate_code())
    vendor = factory.SubFactory(VendorFactory)
    order_date = factory.Faker("date_time_this_month", tzinfo=timezone.utc)
    delivery_date = factory.Faker("date_time_this_month", tzinfo=timezone.utc)
    items = factory.Faker("json")
    quantity = factory.Faker("random_int", min=0, max=100)
    status = factory.Faker(
        "random_element", elements=["Pending", "Completed", "Canceled"]
    )
    quality_rating = factory.Faker("pyfloat", min_value=0, max_value=5)
    issue_date = factory.LazyFunction(datetime.now(tz=timezone.utc).isoformat)
    acknowledgment_date = factory.LazyFunction(datetime.now(tz=timezone.utc).isoformat)
