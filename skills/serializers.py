# =====================================================================================================================
#  Imports 
# =====================================================================================================================
from django.forms import ValidationError 
from rest_framework import serializers 
from utils.helpers import handle_file_update
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
    def to_internal_value(self, data):
        is_update = self.instance is not None
        validator = DynamicValidator(CategorySkill, instance=self.instance if is_update else None)        
        try:
            validation_data = validator.validate(data, CATEGORY_RULES, is_update=is_update)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        return super().to_internal_value(validation_data)
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
    def to_internal_value(self, data):
        is_update = self.instance is not None
        validator = DynamicValidator(Skill, instance=self.instance if is_update else None)        
        try:
            validation_data = validator.validate(data, SKILLS_RULES, is_update=is_update)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        return super().to_internal_value(validation_data)
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





# =====================================================================================================================
# PublicSkillSerializer
# Serializer is for public display of skills
# Used on the front end
# No data modification is allowed.
# =====================================================================================================================
class PublicSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "title", "description", "level", "percentage", "icon", "color"]
        read_only_fields = fields
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# PublicCategorySkillSerializer
# Serializer is used to display skill categories along with their associated skills.
# It is used on the public skills page.
# =====================================================================================================================
class PublicCategorySkillSerializer(serializers.ModelSerializer):
    skills = PublicSkillSerializer(many=True, read_only=True)
    class Meta:
        model = CategorySkill
        fields = ["id", "title", "status",  "skills"]
        read_only_fields = fields
# =====================================================================================================================

