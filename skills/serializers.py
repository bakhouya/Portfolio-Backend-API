# =====================================================================================================================
#  Imports 
# =====================================================================================================================
from django.forms import ValidationError 
from rest_framework import serializers 
from utils.helpers import handle_file_update, hanlde_validator
from utils.validator import DynamicValidator
from .models import CategorySkill, Skill
from .rules import CATEGORY_RULES, SKILLS_RULES
# =====================================================================================================================


# =====================================================================================================================
# CategorySkillSerializer
# This Serializer is responsible for converting CategorySkill model data
# to and from JSON format, and is used in creation, updating, and display operations.
# =====================================================================================================================
class CategorySkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySkill
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    # =====================================================================
    # Dynamic validation
    # Verification rules (CATEGORY_RULES) are applied.
    # Partial update support is included.
    # =====================================================================
    to_internal_value = hanlde_validator(model_class=CategorySkill, rules=CATEGORY_RULES)
    # =====================================================================
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# SkillSerializer
# This Serializer is responsible for managing skills data (Skill)
# It is used in the control panel (Admin) to create and update skills.
# =====================================================================================================================
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', "user"]

    # =====================================================================
    # Dynamic validation
    # Verification rules (CATEGORY_RULES) are applied.
    # Partial update support is included.
    # =====================================================================
    to_internal_value = hanlde_validator(model_class=Skill, rules=SKILLS_RULES)
    # =====================================================================
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
        if "icon" in data:
            handle_file_update(data.get("icon"), instance.icon)
       
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    # =====================================================================
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# =====================================================================================================================
class ActiveSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "title", "icon"]
# =====================================================================================================================



# =====================================================================================================================
# PublicCategorySkillSerializer
# Serializer is used to display skill categories along with their associated skills.
# It is used on the public skills page.
# =====================================================================================================================
class PublicCategorySkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySkill
        fields = ["id", "title",]
        read_only_fields = fields
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# PublicSkillSerializer
# Serializer is for public display of skills
# Used on the front end
# No data modification is allowed. , source="category"
# =====================================================================================================================
class PublicSkillSerializer(serializers.ModelSerializer):
    category = PublicCategorySkillSerializer(read_only=True)
    class Meta:
        model = Skill
        fields = ["id", "title", "description", "level", "percentage", "icon", "color", "category"]
        read_only_fields = fields
# =====================================================================================================================


