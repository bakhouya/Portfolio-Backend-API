# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlatformSettingsView, ContentSettingsView, FaqViewSet, PublicContentView, PublicFaqListView, PublicPlatformView
    )
# ======================================================================================
# 
# 
# 
# ======================================================================================
# default router for GRUD Faq Section
# ======================================================================================
router = DefaultRouter() 
router.register(r'ad/faqs', FaqViewSet, basename='skills')  
# ======================================================================================
# 
# 
# 
# ======================================================================================
# Urls app skills 
# ======================================================================================
urlpatterns = [
    # GRUD Faq Section Endpoints (GET, POST, PUT, PATCH, DELETE)
    path('', include(router.urls)),
    # GET - PUT - PATCH Platform Settings & Content
    path('ad/settings/', PlatformSettingsView.as_view(), name="Settings"),
    path('ad/content/', ContentSettingsView.as_view(), name="Content"),
    # public endpoints = platform settings, content, faqs
    path('public/platform/', PublicPlatformView.as_view(), name="Public_settings"),
    path('public/content/', PublicContentView.as_view(), name="Public_content"),
    path('public/faqs/', PublicFaqListView.as_view(), name="Public_faq"),
]
# ======================================================================================
