# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# ======================================================================================




# ======================================================================================
# default router for GRUD projects & ProjectType sections
# ======================================================================================
router = DefaultRouter()
router.register(r'ad/projects/types', views.ProjectTypeViewSet, basename='projects_types')  
router.register(r'ad/projects', views.ProjectViewSet, basename='projects')  
# ======================================================================================




# ======================================================================================
# Urls app skills 
# ======================================================================================
urlpatterns = [
    
    # include GRUD endoints admin Experiences & Experience types
    path('', include(router.urls)),
    # get list active experience types
    path("ad/projects-types/active/", views.ActiveProjectTypeView.as_view(), name="Active_types"),
    # delete image singal
    path('ad/projects/images/<uuid:pk>/delete/', views.DeleteProjectImageView.as_view(), name='delete_project_image'),


    # # public Projects endpoint
    path("public/projects/", views.PublicProjectView.as_view(), name="Public_projects"),
    # # public Project detail endpoint & register as view by visitor
    path("public/projects/<uuid:pk>/", views.PublicProjectDetailView.as_view(), name="project_details"),
    # liked or unliked project by visitor
    path('public/projects/<uuid:pk>/like/', views.project_like_view, name='project_like'),
   
]
# ======================================================================================
