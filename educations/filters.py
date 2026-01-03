
import django_filters
from .models import Education

# ===================================================================================
# Education filter fields 
# ===================================================================================
class EducationFilter(django_filters.FilterSet):
    # filter by type title or id
    type = django_filters.CharFilter(field_name='type__title', lookup_expr='icontains')
    type_id = django_filters.UUIDFilter(field_name='type__id')
    # filter by institution & location
    institution = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    # filter by status & is current
    status = django_filters.BooleanFilter()
    is_current = django_filters.BooleanFilter()
    # filter by start_date & end_date 
    start_date_gte = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date_lte = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Education
        fields = ['type', 'type_id', 'institution', 'location', 'status', 'is_current', 'is_current', 'start_date_gte', 'end_date_lte']
    
# ===================================================================================
