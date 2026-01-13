# ======================================================================================
# imports 
# ======================================================================================
from django.urls import path
from . import views
# ======================================================================================

urlpatterns = [

    path("ad/statics/total/", views.DashboardStatisticsView.as_view(), name="total statistics"),
    path("ad/statics/source/", views.DetailedSourceAnalysisView.as_view(), name="detailed source analysis"),
    path("ad/statics/top-projects/", views.TopViewedProjectsView.as_view(), name="top viewed projects"),
    path('ad/analytics/visitors/', views.SimpleVisitorsChartView.as_view(), name='visitors-analytics'),
]