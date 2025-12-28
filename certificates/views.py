
from rest_framework import viewsets, permissions, generics
from django.db.models import Prefetch
from skills.models import Skill
from utils.helpers import IsOwnerAdmin
from utils.paginations import CustomDynamicPagination
from .serializers import CertificateSerializer, PublicCertificaleSerializer
from .models import Certificate 


# =====================================================================================================================
# ViewSet for Certificate Management
# Allows administrators to create, edit, and delete Certificates
# IsOwnerAdmin privileges have been added to ensure users can only act on their own data
# When a new skill is created, it is automatically linked to the current user
# =====================================================================================================================
class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsOwnerAdmin]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Public View for Certificates Display
# Accessible to visitors without requiring login
# Displays only active skill Certificate (status=True)
# Fetches the active Certificates associated with each Certificate
# Prefetch_related was used to improve performance and reduce the number of queries
# =====================================================================================================================
class PublicCertificateView(generics.ListAPIView):
    serializer_class = PublicCertificaleSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = Certificate.objects.filter(status=True).prefetch_related(
            Prefetch('skills', queryset=Skill.objects.filter(status=True))
        )
        return queryset
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Public View: Displays details of a single certificate
# Allows visitors to view details of a specific certificate
# Displays only active skills (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicCertificateDetailView(generics.RetrieveAPIView):
    serializer_class = PublicCertificaleSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = Certificate.objects.filter(status=True).prefetch_related(
            Prefetch('skills', queryset=Skill.objects.filter(status=True))
        )
        return queryset
# =====================================================================================================================