


import django_filters
from .models import Project

# ===================================================================================
# Experience filter fields 
# ===================================================================================
class ProjectFilter(django_filters.FilterSet):
    # filter by type title or id
    type = django_filters.CharFilter(field_name='type__title', lookup_expr='icontains')
    type_id = django_filters.UUIDFilter(field_name='type__id')

    skills = django_filters.UUIDFilter(field_name='skills__id')

    # filter by status 
    status = django_filters.BooleanFilter()

    # filter by start_date & end_date 
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    project_date_after  = django_filters.DateFilter(field_name='project_date', lookup_expr='gte')
    project_date_before = django_filters.DateFilter(field_name='project_date', lookup_expr='lte')

    has_github = django_filters.BooleanFilter(field_name='github_url', lookup_expr='isnull', exclude=True)
    has_video = django_filters.BooleanFilter(field_name='video_url', lookup_expr='isnull', exclude=True)
    has_demo = django_filters.BooleanFilter(field_name='demo_url', lookup_expr='isnull', exclude=True)

    class Meta:
        model = Project
        fields = ['type', 'type_id', 'skills', 'status',  'created_after', 'created_before', 
                  'project_date_after', 'project_date_before', 'has_github', "has_video", "has_demo"]
# ===================================================================================
