
# =====================================================================================================================
# imports 
# =====================================================================================================================
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model() # Get User Model 
from django.contrib.auth import update_session_auth_hash
from .models import Profile, About
from utils.validator import DynamicValidator # Import class handle dynamic Validate data 
from utils.helpers import handle_file_update, hanlde_validator, hanlde_validator # import  method handle files(remove old file if updated)
from .rules import CHANGE_PASSWORD_RULES, USER_RULES, PROFILE_RULES, ABOUT_RULES # import rules validations use any model(User, Profile, About)
# =====================================================================================================================





# =====================================================================================================================
# This client verifies login credentials via username and password.
# It checks the user's presence and the validity of the data, then confirms the account status (activated).
# Upon successful verification, it returns the user object within the verified data.
# =====================================================================================================================
class CustomLoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            # check if this user exists if not return this meessage
            if not user:
                raise serializers.ValidationError({"error": "Invalid username  or password"})
            # check if this user active exists if not return this meessage
            if not user.is_active:
                raise serializers.ValidationError({"error": "Your account is deactivated"})
           
        # check if data empty return this message    
        else:
            raise serializers.ValidationError({"error": "Invalid username or password"})

        data["user"] = user
        return data
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# This Serializer is responsible for converting Profile form data
# to and from JSON format for use in APIs.
# All fields are displayed without exception.
# =====================================================================================================================
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile 
        fields = "__all__"
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# This serializer is designed to display basic user data
# and link it to profile data (Nested Serializer).
# Purpose:
# - Returns user data along with their profile in a single response
# - Used to display the portfolio or public profile page
# All fields here are read-only (read_only_fields) to prevent any unintended modification via this serializer.
# =====================================================================================================================
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User 
        fields = fields = ['id', 'username', 'email', 'first_name', 'last_name', "profile"]
        read_only_fields = ['id', 'username', 'email', 'first_name', 'last_name', "profile"]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# This serializer is designed for updating profile data (by the user or administrator).
# It supports:
# Partial updates
# Dynamic data verification based on defined rules
# Handling file updates (profile picture and resume)
# =====================================================================================================================
class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile 
        fields = fields = ['id', 'job_title', 'bio', 'phone', 'avatar', "cv_file", 
                            "github_url", "linkedin_url", "youtube_url", "facebook_url", "instagram_url", "whatsapp_url"]
        read_only_fields = ["id"]

    # =====================================================================
    # Dynamic validation
    # Here:
    # - Determine whether the operation is an update or a creation
    # - Pass data to the DynamicValidator
    # - Apply validation rules (PROFILE_RULES)
    # - Return clear errors if any are found
    # =====================================================================
    to_internal_value = hanlde_validator(model_class=Profile, rules=PROFILE_RULES)
    # =====================================================================
    # 
    # 
    # =====================================================================
    # Handle Update Profile
    # Here:
    # - Delete the old file if a new file is uploaded
    # - Dynamically update the remaining fields
    # - Save the changes in the database
    # =====================================================================
    def update(self, instance, validated_data):
        if "avatar" in validated_data:
            handle_file_update(validated_data.get("avatar"), instance.avatar)

        if "cv_file" in validated_data:
            handle_file_update(validated_data.get("cv_file"), instance.cv_file)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    # =====================================================================
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# This serializer is designed to update basic user data, such as name, email address, and username.
# It does not allow changing the user ID.
# Dynamic verification is used to ensure data accuracy.
# =====================================================================================================================
class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields =  ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ["id"]
    
    # ========================================================================================
    # Custom validator handlier
    # ========================================================================================
    to_internal_value = hanlde_validator(model_class=User, rules=USER_RULES)
    # ========================================================================================

    # =====================================================================
    # Controlling the Format of Response Representation
    # Currently, data is returned as is.
    # In the future, it can be customized or calculated fields can be added.
    # =====================================================================
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
    # =====================================================================

# =====================================================================================================================






# =====================================================================================================================
# AboutSerializer Model about
# this serializer is designed to get and create and update data about section
# =====================================================================================================================
class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    # ========================================================================================
    # Custom validator handlier
    # ========================================================================================
    to_internal_value = hanlde_validator(model_class=About, rules=ABOUT_RULES)
    # ========================================================================================
    # 
    # 
    # =====================================================================
    # Handle Update About
    # Here:
    # - Delete the old file if a new file is uploaded
    # - Dynamically update the remaining fields
    # - Save the changes in the database
    # =====================================================================
    def update(self, instance, data):
        if "image" in data:
            handle_file_update(data.get("image"), instance.image)
       
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    # =====================================================================
# =====================================================================================================================




class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_password"]

    # ========================================================================================
    # Custom validator handlier
    # ========================================================================================
    to_internal_value = hanlde_validator(model_class=User, rules=CHANGE_PASSWORD_RULES)
    # ========================================================================================
    
    def validate(self, data):
        user = self.context["request"].user
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})
        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})
        return data
    
    def save(self, **kwargs):
        user = self.context["request"].user
        new_password = self.validated_data.get("new_password")

        user.set_password(new_password)
        user.save()
        
        return user
