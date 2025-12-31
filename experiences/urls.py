# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ExperienceTypeViewSet, ActiveExperienceTypeView, ExperienceViewSet, PublicExperienceView, PublicExperienceDetailView)
# ======================================================================================

# ======================================================================================
# default router for GRUD Experiences & ExperienceType sections
# ======================================================================================
router = DefaultRouter()
router.register(r'ad/experiences/types', ExperienceTypeViewSet, basename='experiences_types')  
router.register(r'ad/experiences', ExperienceViewSet, basename='experiences')  
# ======================================================================================


# ======================================================================================
# Urls app skills 
# ======================================================================================
urlpatterns = [
    # include GRUD endoints admin Experiences & Experience types
    path('', include(router.urls)),
    # get list active experience types
    path("ad/experiences-types/active/", ActiveExperienceTypeView.as_view(), name="Active_types"),
    # # public Experiences endpoint
    path("public/experiences/", PublicExperienceView.as_view(), name="Public_experiences"),
    # # public Experience detail endpoint
    path("public/experiences/<uuid:pk>/", PublicExperienceDetailView.as_view(), name="experience_details"),
]
# ======================================================================================
