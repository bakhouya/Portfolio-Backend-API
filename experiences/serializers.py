
from rest_framework import serializers
from utils.helpers import handle_file_update, hanlde_validator
from .models import ExperienceType, Experience
from .rules import EXPERIENCE_TYPE_RULES, EXPERIENCE_RULES


# =====================================================================================================================
# ExperienceTypeSerializer
# This Serializer is responsible for converting ExperienceType model data
# to and from JSON format, and is used in creation, updating, and display operations.
# =====================================================================================================================
class ExperienceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceType
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=ExperienceType, rules=EXPERIENCE_TYPE_RULES)
    # ===============================================================================================================
# =====================================================================================================================
# =====================================================================================================================
class TypeExperienceSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceType
        fields = ["id", "title"]
        read_only_fields = ["id", "title"]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# ExperienceSerializer
# This Serializer is responsible for converting Experience model data
# to and from JSON format, and is used in creation, updating, and display operations.
# =====================================================================================================================
class ExperienceSerializer(serializers.ModelSerializer):
    type_details = TypeExperienceSerialzer(read_only=True, source="type")
    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', "user", "type_details"]

    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=Experience, rules=EXPERIENCE_RULES)
    # ===============================================================================================================
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
        if "logo" in data:
            handle_file_update(data.get("logo"), instance.logo)
       
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    # =====================================================================
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# PublicExperinceSerializer : for get public experiences view
# =====================================================================================================================
class PublicExperinceSerializer(serializers.ModelSerializer):
    type_details = TypeExperienceSerialzer(read_only=True, source="type")
    class Meta:
        model = Experience
        fields = '__all__'
# =====================================================================================================================
