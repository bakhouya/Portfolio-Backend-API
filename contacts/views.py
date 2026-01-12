
# =================================================================================
# =================================================================================
from rest_framework import permissions, viewsets, generics
from django.contrib.auth import get_user_model
User = get_user_model()
from utils.paginations import CustomDynamicPagination
from .serializers import  ContactSerializer
from .models import Contact
# =================================================================================


# =====================================================================================================================
# ViewSet for managing Contact
# This ViewSet is for Admin only
# Allows creating, editing, deleting, and all types of skill resorting
# Uses an electronic migration system for splitting results
# =====================================================================================================================
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
# =====================================================================================================================
# 
# 
# 
# =====================================================================================================================
# Geerics For Create New Contact Info
# This View is for anyone 
# =====================================================================================================================
class AdminContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
# =====================================================================================================================




