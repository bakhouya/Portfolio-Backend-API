# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ActiveSkillsView, CategorySkillsViewSet, SkillsViewSet, PublicSkillsView, PublicSkillDetailView)
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
    # active skills for created admin
    path("ad/skills/active/", ActiveSkillsView.as_view(), name="Active_Skills"),
    # include GRUD endoints admin skills & categorySkill
    path('', include(router.urls)),
    # public skills endpoint
    path("public/skills/", PublicSkillsView.as_view(), name="Public_Skills"),
    # public skills detail endpoint
    path("public/skills/<uuid:pk>/", PublicSkillDetailView.as_view(), name="Skill_details"),
]
# ======================================================================================
