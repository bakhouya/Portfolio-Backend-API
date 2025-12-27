# =====================================================================================================================
# Imports 
# =====================================================================================================================
from django.forms import ValidationError 
from rest_framework import generics, status, viewsets 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile, About
from .serializers import (CustomLoginUserSerializer, UserSerializer, UpdateProfileSerializer, UpdateUserSerializer, AboutSerializer)
from utils.paginations import CustomDynamicPagination
from utils.helpers import IsOwnerAdmin
# =====================================================================================================================
   







# =====================================================================================================================
# This interface handles the login process using APIView in a flexible manner.
# Upon successful authentication, it returns the verification tokens required to access protected interfaces.
# It also returns the login credentials of the user who performed the login.
# =====================================================================================================================
class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_403_FORBIDDEN if "Blocked" in str(e.detail) else status.HTTP_400_BAD_REQUEST) 
        
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        user_permissions = []
        for group in user.groups.all():
            for permission in group.permissions.all():
                user_permissions.append(permission.codename)

        for permission in user.user_permissions.all():
            user_permissions.append(permission.codename)
        
        user_permissions = list(set(user_permissions))
        # handle response token & data user if auth success
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "is_active": user.is_active,
                "groups": [group.name for group in user.groups.all()],
                "permissions": user_permissions 
            }
        }, status=status.HTTP_200_OK)
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# This view is for managing the Admin User's data.
# Only an authenticated user (IsAuthenticated) with administrator privileges (IsAdminUser) is allowed to view and update their personal data.
# Objective:
# == Enable the administrator to retrieve their account data (GET).
# == Enable the administrator to partially modify their account data (PUT/PATCH).
# Working Process:
# == The current user (request.user) is always accessed.
# == Data from other users cannot be accessed.
# Outcome:
# == Upon a successful request, the user's data is returned in JSON format.
# == Upon updating, changes are saved, and the updated data is returned.
# =====================================================================================================================
class AdminUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# This view is for managing the administrator user's profile.
# Only an authenticated administrator can view and update their profile.
# Objective:
# == To retrieve the profile data associated with the current user.
# == To edit profile data such as the picture or additional information.
# Workflow:
# == The profile associated with request.user is searched for.
# == If no profile is found, a 404 error is returned.
# Result:
# == The profile data is returned in JSON format.
# == The data is updated upon request and verified.
# =====================================================================================================================
class AdminProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  
    
    def get_object(self):
        return generics.get_object_or_404(Profile, user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# This view is designed to display portfolio data to visitors.
# It requires no permissions (AllowAny) and can be accessed by any user or visitor.
# Objective:
# == Displays the primary portfolio owner's data on the website.
# == Used on the front-end to display general information (Portfolio Page).
# Working Process:
# == The first active user (is_active=True) is retrieved from the database.
# == The system assumes only one user, representing the portfolio owner.
# Result: The user's data is returned in JSON format for display on the front-end.
# =====================================================================================================================
class PortfolioView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        return User.objects.filter(is_active=True).first()
# =====================================================================================================================





# =====================================================================================================================
# ViewSet for Admin Management of the "About" Section.
# Purpose:
# - Enables admins to create, edit, delete, and view About section data.
# - Links each record to the user who created it.
# Permissions:
# - IsAuthenticated: Must be logged in.
# - IsAdminUser: Must be an admin.
# - IsOwnerAdmin: Can only edit data owned by the user.
# Properties:
# - pagination_class: Dynamically segments results.
# - queryset: Fetches all About records.
# - serializer_class: Converts data to and from JSON.
# Outcome:
# - A secure, full-featured API (CRUD) for managing About content from the control panel.
# =====================================================================================================================
class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [IsAuthenticated, IsAdminUser, IsOwnerAdmin]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# ViewSet is a public interface for displaying the About section.
# Objective:
# - To allow any visitor to view About content.
# - Without allowing any modification or deletion.
# Permissions:
# - AllowAny: Available to everyone (even unregistered users).
# Properties:
# - ReadOnlyModelViewSet: Allows only (list, retrieve).
# - pagination_class: Splits results to improve performance.
# Outcome:
# - A public and secure API for displaying About content on a website or application.
# =====================================================================================================================
class PublicAboutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    pagination_class = CustomDynamicPagination
    permission_classes = [AllowAny]  
# =====================================================================================================================
