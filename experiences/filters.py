
import django_filters
from .models import Experience

# ===================================================================================
# Experience filter fields 
# ===================================================================================
class ExperienceFilter(django_filters.FilterSet):
    # filter by type title or id
    type = django_filters.CharFilter(field_name='type__title', lookup_expr='icontains')
    type_id = django_filters.UUIDFilter(field_name='type__id')
    # filter by status & is current
    status = django_filters.BooleanFilter()
    is_current = django_filters.BooleanFilter()
    # filter by start_date & end_date 
    start_date_gte = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date_lte = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Experience
        fields = ['type', 'status', 'is_current', 'type_id', 'type', 'status', 'is_current', 'start_date_gte', 'end_date_lte']
# ===================================================================================
