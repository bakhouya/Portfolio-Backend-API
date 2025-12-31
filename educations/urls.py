# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EducationTypeViewSet,ActiveEducationTypeView, EducationViewSet, PublicEducationView, PublicEducationDetailView)
# ======================================================================================

# ======================================================================================
# default router for GRUD skills & categorySkill sections
# ======================================================================================
router = DefaultRouter()
router.register(r'ad/educations/types', EducationTypeViewSet, basename='education_types')  
router.register(r'ad/educations', EducationViewSet, basename='educations')  
# ======================================================================================


# ======================================================================================
# Urls app skills 
# ======================================================================================
urlpatterns = [
    # include GRUD endoints admin educations & education types
    path('', include(router.urls)),
    path("ad/educations/types/active/", ActiveEducationTypeView.as_view(), name="Active_types"),
    # # public educations endpoint
    path("public/educations/", PublicEducationView.as_view(), name="Public_educations"),
    # # public education detail endpoint
    path("educations/<uuid:pk>/", PublicEducationDetailView.as_view(), name="Education_details"),
]
# ======================================================================================
