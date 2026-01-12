

# ======================================================================================
# imports 
# ======================================================================================
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# ======================================================================================
# 
# 
# ======================================================================================
# default router for GRUD contact messages
# ======================================================================================
router = DefaultRouter() 
router.register(r'ad/messages', views.ContactViewSet, basename='messages')  
# ======================================================================================
# 
# 
urlpatterns = [
    # include routes GRUD Admin 
    path('', include(router.urls)),
    # Endpoints Create Contact Message for Client
    path("public/messages/", views.AdminContactCreateView.as_view(), name="public messages"),
]

