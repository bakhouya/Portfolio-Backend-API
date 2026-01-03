

from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import ProjectImage, ProjectType, Project
from .serializers import ProjectImageSerializer, ProjectTypeSerializer, ProjectSerializer
from utils.paginations import CustomDynamicPagination
from visitors.models import Visitor
from .filters import ProjectFilter



# =====================================================================================================================
# ViewSet for managing ProjectType 
# This ViewSet is for Admin only
# Allows creating, editing, deleting, and all types of ProjectType resorting
# Uses an electronic migration system for splitting results
# =====================================================================================================================
class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = CustomDynamicPagination
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Get list active project types
# =====================================================================================================================
class ActiveProjectTypeView(generics.ListAPIView):
    queryset = ProjectType.objects.filter(status=True)
    serializer_class = ProjectTypeSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# handler all GRUD project : create, get, update, delete
# this viewsets for auth and admin user 
# =====================================================================================================================
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['title', 'details', 'description']
    ordering_fields = ['project_date', 'created_at', 'updated_at', "likes", "views"]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# View for delete singal image 
# this view is for auth & admin user 
# =====================================================================================================================
class DeleteProjectImageView(generics.DestroyAPIView):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
# =====================================================================================================================





# =====================================================================================================================
# Public View: Displays all list Projects
# Allows visitors to view tlist of a specific Projects
# Displays only active Projects (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicProjectView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['title', 'details', 'description']
    ordering_fields = ['project_date', 'created_at', 'updated_at', "likes", "views"]
    def get_queryset(self):
        queryset = Project.objects.filter(status=True)
        return queryset
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# Public View: Displays details of a single Project
# Allows visitors to view details of a specific Project
# Displays only active Project (status=True)
# Requires no permissions or authentication
# =====================================================================================================================
class PublicProjectDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Project.objects.filter(status=True)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.record_view(instance, request)
        response = super().retrieve(request, *args, **kwargs)      
        return response
    
    def record_view(self, project, request):
        visitor_id = request.GET.get('visitor')

        if not visitor_id:
            return False
        
        try:
            visitor = Visitor.objects.get(id=visitor_id)
            if visitor: 
                if not project.views.filter(id=visitor.id).exists():
                    project.views.add(visitor)
                    return True
                return False
        except Visitor.DoesNotExist:
            return False
      
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# method handler like or unliked project by visitor
# =====================================================================================================================
@api_view(['POST'])
def project_like_view(request, pk):
    # ================================================================================================
    # get project item by id (pk)
    # if not exists return 404 status & error message (not found)
    # ================================================================================================
    try:
        project = Project.objects.get(id=pk, status=True)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    # ================================================================================================
    
    # ================================================================================================
    # get visitor id from query params or request data
    # if not provided return 404 status & error message (visitor id is required)
    # ================================================================================================
    visitor_id = request.query_params.get('visitor') or request.data.get('visitor')   
    if not visitor_id:
        return Response({"error": "Visitor ID is required"},  status=status.HTTP_400_BAD_REQUEST)
    # ================================================================================================
    
    # ================================================================================================
    # try to get visitor by id 
    # if project has already been liked by visitor, remove like (unlike)
    # if project has not been liked by visitor, add like 
    # return success message with current liked count
    try:
        visitor = Visitor.objects.get(id=visitor_id)
        
        if project.likes.filter(id=visitor.id).exists():
            project.likes.remove(visitor)
            action_msg = "unliked"
        else:
            project.likes.add(visitor)
            action_msg = "liked"
        
        return Response({  
            "success": True,
            "message": f"Project {action_msg} successfully",
            "likes_count": project.likes.count(),
        }, status=status.HTTP_200_OK)
        
    except Visitor.DoesNotExist:
        return Response({"error": "Visitor not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)},  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # ================================================================================================
# =====================================================================================================================
  