# =========================================================================================
#  imports
# =========================================================================================
from rest_framework import  permissions, generics, viewsets 
from .serializers import (
    PlatformSerializer, ContentSerializer, FaqSerializer, PublicPlatformSerializer, PublicContentSerializer, PublicFaqSerializer
)
from .models import PlatformSettings, Content, Faq
# =========================================================================================




# =========================================================================================
# Platform Settings View
# Purpose:
# - Enable the Admin to fetch and update general platform settings
# such as: title, description, logos, contact information...
# Permissions:
# - Available only to registered users
# - The user must be an Admin
# # Outcome:
# - GET: Reverts to the current platform settings (one record only)
# - PUT/PATCH: Updates the same settings without creating a new record
# =========================================================================================
class PlatformSettingsView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = PlatformSerializer
    
    def get_object(self):
        return PlatformSettings.get_settings()
# =========================================================================================
# 
# 
# =========================================================================================
# View Site Content Settings
# Purpose:
# - Control the display or hiding of site sections
# such as: About, Skills, Projects, Experience, Education...
# - Control the titles and descriptions of these sections
# Permissions:
# - Available only to registered users
# - The user must be an administrator (Admin)
# # Outcome:
# - GET: Reverts to the current content settings
# - PUT/PATCH: Updates content settings without creating a new record
# =========================================================================================
class ContentSettingsView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = ContentSerializer
    ContentSerializer
    def get_object(self):
        return Content.get_content()
# =========================================================================================
# 
# 
# =========================================================================================
# ViewSet for Frequently Asked Questions (FAQs) Management
# Purpose:
# - Enable administrators to create, edit, delete, and view FAQs
# Permissions:
# - Available only to registered users
# - User must be an administrator (Admin)
# Outcome: # - Full CRUD on FAQs via the admin panel or API
# =========================================================================================
class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
# =========================================================================================




# =========================================================================================
# Public Platform Settings View
# Purpose:
# - Enable visitors to view public platform settings
# such as: title, description, logos, contact information
#
# Permissions:
# - Available to everyone (no registration required)
# # Outcome:
# - GET only: Returns the frontend platform settings
# =========================================================================================
class PublicPlatformView(generics.RetrieveAPIView):
    serializer_class = PublicPlatformSerializer
    permission_classes = [permissions.AllowAny] 
    
    def get_object(self):
        return PlatformSettings.get_settings()
# =========================================================================================
# 
# 
# =========================================================================================
# Public Content Settings View
#Purpose:
# - Enable the front-end to know:
# - Which sections are enabled or hidden
# - Titles and descriptions for each section
#Permissions:
# - Accessible to everyone (no registration required)
#Outcome:
# - GET only: Revert content settings for use on the site
# =========================================================================================
class PublicContentView(generics.RetrieveAPIView):
    serializer_class = PublicContentSerializer
    permission_classes = [permissions.AllowAny]    
    def get_object(self):
        return Content.get_content()
# =========================================================================================
# 
# 
# =========================================================================================
# Public FAQ List View
# Objective:
# - Enable visitors to view frequently asked questions
# without requiring login
# Permissions:
# - Allow anyone
# Outcome:
# - GET: Returns a list of all frequently asked questions
# =========================================================================================
class PublicFaqListView(generics.ListAPIView):
    queryset = Faq.objects.all()
    serializer_class = PublicFaqSerializer
    permission_classes = [permissions.AllowAny]  
# =========================================================================================
