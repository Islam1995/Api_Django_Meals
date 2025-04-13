import django_filters
from .models import Product

class ProductFilters(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.filters.CharFilter(field_name='name',lookup_expr='icontains')
    minprice = django_filters.filters.NumberFilter(field_name='price' or 0, lookup_expr='gte')
    maxprice = django_filters.filters.NumberFilter(field_name='price' or 100000, lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['minprice','Catogery', 'brand','keyword','maxprice',]