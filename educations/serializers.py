
from rest_framework import serializers
from utils.helpers import handle_file_update, hanlde_validator
from .models import EducationType, Education
from .rules import EDUCATION_TYPE_RULES, EDUCATION_RULES


# =====================================================================================================================
# EducationTypeSerializer
# This Serializer is responsible for converting EducationType model data
# to and from JSON format, and is used in creation, updating, and display operations.
# =====================================================================================================================
class EducationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationType
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=EducationType, rules=EDUCATION_TYPE_RULES)
    # ===============================================================================================================
# =====================================================================================================================
# =====================================================================================================================
class TypeEducationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = EducationType
        fields = ["id", "title"]
        read_only_fields = ["id", "title"]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# EducationTypeSerializer
# This Serializer is responsible for converting EducationType model data
# to and from JSON format, and is used in creation, updating, and display operations.
# =====================================================================================================================
class EducationSerializer(serializers.ModelSerializer):
    type_details = TypeEducationSerialzer(read_only=True, source="type")
    class Meta:
        model = Education
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', "user", "type_details"]

    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=Education, rules=EDUCATION_RULES)
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



class PublicEducationSerializer(serializers.ModelSerializer):
    skills = TypeEducationSerialzer(read_only=True, source="type")
    class Meta:
        model = Education
        fields = '__all__'