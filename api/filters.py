import django_filters
from api.models import Product
from rest_framework import filters

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'price': ['exact', 'lt', 'gt', 'lte', 'gte', 'range'],
            'stock': ['exact', 'lt', 'gt', 'lte', 'gte', 'range'],
        }
      
        
class InStockFilterBackend(filters.BaseFilterBackend):
    """
    Custom filter to return only products that are in stock.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)