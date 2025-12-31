
import django_filters
from .models import Education
from django.db.models import Q

# ===================================================================================
# Education filter fields 
# ===================================================================================
class EducationFilter(django_filters.FilterSet):
    # multi searching fields
    search = django_filters.CharFilter(method='filter_search')
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
        fields = ['type', 'institution', 'location', 'status', 'is_current', 'search', 'type_id', 'type', 'status', 'is_current', 'start_date_gte', 'end_date_lte']
    
    # method multi searching
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(field_of_study__icontains=value) |
            Q(description__icontains=value) |
            Q(institution__icontains=value) |
            Q(location__icontains=value)
        )
# ===================================================================================
