
# ================================================================================================
# Imports
# ================================================================================================
from urllib import request
from rest_framework import serializers
from .models import ProjectType, Project, ProjectImage
from skills.models import Skill
from visitors.models import Visitor
from utils.helpers import hanlde_validator
from .rules import PROJECT_TYPES_RULES, PROJECT_RULES
# ================================================================================================



# ================================================================================================
# ProjectTypeSerializer 
# ================================================================================================
class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'
        read_only_fields = ["id", "created_at", "updated_at"]
    
    # ========================================================================================
    # Custom validator handlier
    # ========================================================================================
    to_internal_value = hanlde_validator(model_class=ProjectType, rules=PROJECT_TYPES_RULES)
    # ========================================================================================
# ================================================================================================
# 
# ================================================================================================
# TypeProjectSerialzer
# ================================================================================================
class TypeProjectSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ["id", "title"]
        read_only_fields = ["id", "title"]
# ================================================================================================
# 
# ================================================================================================
# ProjectSkillsSerializer
# ================================================================================================
class ProjectSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "title", "icon"]
        read_only_fields = ["id", "title", "icon"]
# ================================================================================================
# 
# ================================================================================================
# ProjectImageSerializer
# ================================================================================================
class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']
        read_only_fields = ['id', "image"]
# ================================================================================================




# ================================================================================================
# ProjectSerializer
# ================================================================================================
class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    type = serializers.UUIDField(write_only=True)
    skills = serializers.ListField(child=serializers.UUIDField(), write_only=True)
    images = serializers.ListField(write_only=True)

    type_details = TypeProjectSerialzer(read_only=True, source="type")  
    skills_details = ProjectSkillsSerializer(many=True, read_only=True, source="skills") 
    images_details = ProjectImageSerializer(many=True, read_only=True, source="images")
    
    likes_count = serializers.SerializerMethodField(read_only=True)
    views_count = serializers.SerializerMethodField(read_only=True)

    is_liked = serializers.SerializerMethodField(read_only=True)
    is_viewed = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Project
        fields = ["id", "user", "type", "type_details", "title", "description", "details", "skills", "skills_details", "images", "images_details",
                  "is_liked", "is_viewed", "likes_count", "views_count", "project_date", "demo_url", "github_url", "video_url", "status", "created_at", "updated_at"]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    # ========================================================================================
    # Custom validator handlier
    # ========================================================================================
    to_internal_value = hanlde_validator(model_class=Project, rules=PROJECT_RULES)
    # ========================================================================================
    # 
    # ========================================================================================
    # get likes count
    # ========================================================================================
    def get_likes_count(self, object):
        return object.likes.count()
    # ========================================================================================
    # 
    # ========================================================================================
    # get views count
    # ========================================================================================
    def get_views_count(self, object):
        return object.views.count()
    # ========================================================================================
    # 
    # ========================================================================================
    # check if visitor has already liked this object project
    # ========================================================================================
    def get_is_liked(self, object):
        request = self.context.get('request')
        if request:
            visitor_hash = request.COOKIES.get('visitor_hash')
            if visitor_hash:
                try:
                    visitor = Visitor.objects.get(key=visitor_hash)
                    return object.likes.filter(id=visitor.id).exists()
                except Visitor.DoesNotExist:
                    return False
        return False
    # ========================================================================================
    # 
    # ========================================================================================
    # check if visitor has already view this object project
    # ========================================================================================
    def get_is_viewed(self, object):
        request = self.context.get('request')
        if request:
            visitor_hash = request.COOKIES.get('visitor_hash')
            if visitor_hash:
                try:
                    visitor = Visitor.objects.get(key=visitor_hash)
                    return object.views.filter(id=visitor.id).exists()
                except Visitor.DoesNotExist:
                    return False
        return False
    # ========================================================================================
    # 
    # ========================================================================================
    # handle create new project with skills and images
    # ========================================================================================
    def create(self, data):
        # pop type uuid from data request body and get him from database if exists
        type_uuid = data.pop('type')
        try:
            project_type = ProjectType.objects.get(id=type_uuid)
        except ProjectType.DoesNotExist:
            raise serializers.ValidationError({"type": "Invalid project type ID."})
        #  pop skills and images from data requset body
        skills = data.pop('skills', [])
        images = data.pop('images', [])
        # created and save project in databse
        project = Project.objects.create(type=project_type, **data)
        # save skills in database 
        if skills:
            skills = Skill.objects.filter(id__in=skills)
            project.skills.set(skills)
        # save images in databse
        for image in images:
            ProjectImage.objects.create(project=project, image=image)
        
        return project
    # ========================================================================================
    # 
    # ========================================================================================
    # handler update project 
    # ========================================================================================
    def update(self, instance, data):
        # check if has type field in data if has been pop him and get from databse 
        if 'type' in data:
            type_uuid = data.pop('type')
            try:
                project_type = ProjectType.objects.get(id=type_uuid)
                instance.type = project_type
            except ProjectType.DoesNotExist:
                raise serializers.ValidationError({"type": "Invalid project type ID."})
        
        # Handle skills update
        if 'skills' in data:
            skill_ids = data.pop('skills')
            skills = Skill.objects.filter(id__in=skill_ids)
            instance.skills.set(skills)
        
        # Handle images update
        if 'images' in data:
            uploaded_images = data.pop('images')
            for image in uploaded_images:
                ProjectImage.objects.create(project=instance, image=image)
        
        # Update other fields
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    # ========================================================================================

# ================================================================================================






