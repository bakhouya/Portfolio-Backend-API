
# =====================================================================================================================
# Imports
# =====================================================================================================================
from rest_framework import viewsets, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from utils.paginations import CustomDynamicPagination
from .serializers import (ServiceSerializer)
from .models import Service
# =====================================================================================================================



# =====================================================================================================================
# ViewSet for Service Management
# Allows administrators to create, edit, and delete Services
# IsOwnerAdmin privileges have been added to ensure users can only act on their own data
# When a new Service is created, it is automatically linked to the current user
# =====================================================================================================================
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', "color"]
    ordering_fields = ['created_at', 'title']
# =====================================================================================================================


# =====================================================================================================================
# Public View: Displays all list active Services
# Allows visitors to view tlist of a specific Services
# Displays only active Services (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicServiceView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = Service.objects.filter(status=True)
        return queryset
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Public View: Displays details of a single Active Service
# Allows visitors to view details of a specific Service
# Displays only active Service (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicServiceDetailView(generics.RetrieveAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = Service.objects.filter(status=True)
        return queryset
# =====================================================================================================================
