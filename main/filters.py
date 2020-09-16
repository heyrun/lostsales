import django_filters
from django_filters import DateFilter

from .models import *


class productFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(
        field_name='description', lookup_expr='icontains')
    # # start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    # end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        model = Products
        fields = ['description']


class lostSalesFilter(django_filters.FilterSet):

    start_date = DateFilter(label='From date ("yyyy-mm-dd")', field_name='created_date', lookup_expr='gte'
                            )
    end_date = DateFilter(
        label='End date', field_name='created_date', lookup_expr='lte')

    class Meta:
        model = Lostsales
        fields = ['start_date']
