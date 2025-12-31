from rest_framework import viewsets, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from utils.paginations import CustomDynamicPagination
from .serializers import (ExperienceTypeSerializer, ExperienceSerializer, PublicExperinceSerializer)
from .models import ExperienceType, Experience
from .filters import ExperienceFilter


# =====================================================================================================================
# ViewSet for managing ExperienceType 
# This ViewSet is for Admin only
# Allows creating, editing, deleting, and all types of ExperienceType resorting
# Uses an electronic migration system for splitting results
# =====================================================================================================================
class ExperienceTypeViewSet(viewsets.ModelViewSet):
    queryset = ExperienceType.objects.all()
    serializer_class = ExperienceTypeSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Get list active experinece types
# =====================================================================================================================
class ActiveExperienceTypeView(generics.ListAPIView):
    queryset = ExperienceType.objects.filter(status=True)
    serializer_class = ExperienceTypeSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# ViewSet for Experience Management
# Allows administrators to create, edit, and delete Experience(formation)
# IsOwnerAdmin privileges have been added to ensure users can only act on their own data
# When a new experience is created, it is automatically linked to the current user
# =====================================================================================================================
class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExperienceFilter
    search_fields = ['title', 'company', 'description']
    ordering_fields = ['start_date', 'created_at', 'updated_at']
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# =====================================================================================================================




# =====================================================================================================================
# Public View: Displays all list Experiences
# Allows visitors to view tlist of a specific Experiences
# Displays only active Experiences (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicExperienceView(generics.ListAPIView):
    serializer_class = PublicExperinceSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = Experience.objects.filter(status=True)
        return queryset
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Public View: Displays details of a single Experience
# Allows visitors to view details of a specific Experience
# Displays only active Experience (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicExperienceDetailView(generics.RetrieveAPIView):
    serializer_class = PublicExperinceSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = Experience.objects.filter(status=True)
        return queryset
# =====================================================================================================================