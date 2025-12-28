# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CertificateViewSet, PublicCertificateView, PublicCertificateDetailView)
# ======================================================================================
# 
# 
# 
# ======================================================================================
# default router for GRUD certificates
# ======================================================================================
router = DefaultRouter() 
router.register(r'ad/certificates', CertificateViewSet, basename='Certificates')  
# ======================================================================================
# 
# 
# 
# ======================================================================================
# Urls app skills 
# ======================================================================================
urlpatterns = [
    # GRUD Certificates Endpoints (GET, POST, PUT, PATCH, DELETE)
    path('', include(router.urls)),
    # public get all active certificates
    path('public/certificates/', PublicCertificateView.as_view(), name="Public_certificates"),
    # get singal active certificate details
    path('public/certificates/<uuid:pk>/', PublicCertificateDetailView.as_view(), name="Public_certificate_details"),
]
# ======================================================================================
