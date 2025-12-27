
# =====================================================================================================================
#  imports
# =====================================================================================================================
from rest_framework import viewsets, generics # API Views
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny # permissions
from django.db.models import Prefetch
from utils.helpers import IsOwnerAdmin # permissions Owner
from utils.paginations import CustomDynamicPagination

from skills.models import CategorySkill, Skill # Import Models 
# import Serializers Skills and CategorySkill
from .serializers import CategorySkillSerializer, SkillSerializer, PublicCategorySkillSerializer, PublicSkillSerializer
# =====================================================================================================================



# =====================================================================================================================
# ViewSet for managing skill categories (CategorySkill)
# This ViewSet is for Admin only
# Allows creating, editing, deleting, and all types of skill resorting
# Uses an electronic migration system for splitting results
# =====================================================================================================================
class CategorySkillsViewSet(viewsets.ModelViewSet):
    queryset = CategorySkill.objects.all()
    serializer_class = CategorySkillSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [IsAuthenticated, IsAdminUser]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# ViewSet for Skill Management
# Allows administrators to create, edit, and delete skills
# IsOwnerAdmin privileges have been added to ensure users can only act on their own data
# When a new skill is created, it is automatically linked to the current user
# =====================================================================================================================
class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [IsAuthenticated, IsAdminUser, IsOwnerAdmin]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# =====================================================================================================================





# =====================================================================================================================
# Public View for Skills Display
# Accessible to visitors without requiring login
# Displays only active skill categories (status=True)
# Fetches the active skills associated with each category
# Prefetch_related was used to improve performance and reduce the number of queries
# =====================================================================================================================
class PublicSkillsView(generics.ListAPIView):
    serializer_class = PublicCategorySkillSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = CategorySkill.objects.filter(status=True).prefetch_related(
            Prefetch('skills', queryset=Skill.objects.filter(status=True))
        )
        return queryset
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Public View: Displays details of a single skill
# Allows visitors to view details of a specific skill
# Displays only active skills (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicSkillDetailView(generics.RetrieveAPIView):
    serializer_class = PublicSkillSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = Skill.objects.filter(status=True)
        return queryset
# =====================================================================================================================
