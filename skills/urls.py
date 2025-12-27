# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategorySkillsViewSet, SkillsViewSet, PublicSkillsView, PublicSkillDetailView)
# ======================================================================================

# ======================================================================================
# default router for GRUD skills & categorySkill sections
# ======================================================================================
router = DefaultRouter()
router.register(r'ad/skills/categories', CategorySkillsViewSet, basename='categories_skills')  
router.register(r'ad/skills', SkillsViewSet, basename='skills')  
# ======================================================================================


# ======================================================================================
# Urls app skills 
# ======================================================================================
urlpatterns = [
    # include GRUD endoints admin skills & categorySkill
    path('', include(router.urls)),
    # public skills endpoint
    path("skills/", PublicSkillsView.as_view(), name="Public_Skills"),
    # public skills detail endpoint
    path("skills/<uuid:pk>/", PublicSkillDetailView.as_view(), name="Skill_details"),
]
# ======================================================================================
