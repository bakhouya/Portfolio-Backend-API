
from rest_framework import serializers
from utils.helpers import handle_file_update, hanlde_validator
from .models import Service
from .rules import SERVICE_RULES


# ===============================================================================================
# ServiceSerializer for all GRUD operations and public views
# ===============================================================================================
class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ["id", "created_at", "updated_at"]
    
    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=Service, rules=SERVICE_RULES)
    # ===============================================================================================================
    # 
    # 
    # ===============================================================================================================
    # Handle Update About
    # Here:
    # - Delete the old file if a new file is uploaded
    # - Dynamically update the remaining fields
    # - Save the changes in the database
    # ===============================================================================================================
    def update(self, instance, data):
        if "image" in data:
            handle_file_update(data.get("image"), instance.image)
       
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    # ===============================================================================================================

# ===============================================================================================
