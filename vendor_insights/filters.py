from django_filters import FilterSet, CharFilter
from .models import PurchaseOrder

class PurchaseOrderFilter(FilterSet):
    vendor = CharFilter(field_name='vendor__name', lookup_expr='icontains')
    
    class Meta:
        model = PurchaseOrder
        fields = ['vendor']