
from rest_framework import viewsets, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from utils.paginations import CustomDynamicPagination
from .serializers import (EducationTypeSerializer, EducationSerializer, PublicEducationSerializer)
from .models import EducationType, Education
from .filters import EducationFilter

# =====================================================================================================================
# ViewSet for managing skill categories (CategorySkill)
# This ViewSet is for Admin only
# Allows creating, editing, deleting, and all types of skill resorting
# Uses an electronic migration system for splitting results
# =====================================================================================================================
class EducationTypeViewSet(viewsets.ModelViewSet):
    queryset = EducationType.objects.all()
    serializer_class = EducationTypeSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# =====================================================================================================================
class ActiveEducationTypeView(generics.ListAPIView):
    serializer_class = EducationTypeSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get_queryset(self):
        queryset = EducationType.objects.filter(status=True)
        return queryset
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# ViewSet for education Management
# Allows administrators to create, edit, and delete education(formation)
# IsOwnerAdmin privileges have been added to ensure users can only act on their own data
# When a new education is created, it is automatically linked to the current user
# =====================================================================================================================
class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EducationFilter
    search_fields = ['field_of_study', 'institution', 'description', 'location']
    ordering_fields = ['start_date', 'created_at', 'updated_at']
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# ====================================================================================================================



# =====================================================================================================================
# Public View: Displays all list Educations
# Allows visitors to view tlist of a specific Education
# Displays only active Educations (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicEducationView(generics.ListAPIView):
    serializer_class = PublicEducationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EducationFilter
    search_fields = ['field_of_study', 'institution', 'description', 'location']
    ordering_fields = ['start_date', 'created_at', 'updated_at']
    def get_queryset(self):
        queryset = Education.objects.filter(status=True)
        return queryset
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Public View: Displays details of a single Education
# Allows visitors to view details of a specific Education
# Displays only active Education (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicEducationDetailView(generics.RetrieveAPIView):
    serializer_class = PublicEducationSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = Education.objects.filter(status=True)
        return queryset
# =====================================================================================================================
