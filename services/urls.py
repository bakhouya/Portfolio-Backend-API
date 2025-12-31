

# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ServiceViewSet, PublicServiceView, PublicServiceDetailView)
# ======================================================================================

# ======================================================================================
# default router for GRUD Services sections
# ======================================================================================
router = DefaultRouter()
router.register(r'ad/services', ServiceViewSet, basename='services')  
# ======================================================================================


# ======================================================================================
# Urls app Services 
# ======================================================================================
urlpatterns = [
    # include GRUD endoints admin Services
    path('', include(router.urls)),
    # # public Services endpoint
    path("public/services/", PublicServiceView.as_view(), name="Public_experiences"),
    # # public Service detail endpoint
    path("public/services/<uuid:pk>/", PublicServiceDetailView.as_view(), name="experience_details"),
]
# ======================================================================================
