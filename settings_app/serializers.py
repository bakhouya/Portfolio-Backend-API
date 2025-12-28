
# ======================================================================================
# imports
# ======================================================================================
from config import settings
from rest_framework import serializers
from settings_app.rules import PLATFORM_SETTINGS_RULES, CONTENT_RULES, FAQ_RULES
from utils.helpers import handle_file_update, hanlde_validator
from .models import PlatformSettings, Content, Faq
# ======================================================================================


# ======================================================================================
# Serializer Platform Settings
# ======================================================================================
class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformSettings
        fields = ["id", "title", "description", "dark_logo", "light_logo", "favicon", "contact_email", "support_email", "phone"]
        read_only_fields = ["id", "updated_at"]
  
    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=PlatformSettings, rules=PLATFORM_SETTINGS_RULES)
    # ===============================================================================================================
    # 
    # 
    # ===============================================================================================================
    # handler update to manage file fields 
    # if files are updated, old files are deleted from the storage "media/"
    # ===============================================================================================================
    def update(self, instance, validated_data):
        if "dark_logo" in validated_data:
            handle_file_update(validated_data.get("dark_logo"), instance.dark_logo) 
        if "light_logo" in validated_data:
            handle_file_update(validated_data.get("light_logo"), instance.light_logo)
        if "favicon" in validated_data:
            handle_file_update(validated_data.get("favicon"), instance.favicon) 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    # ===============================================================================================================
# ======================================================================================
# 
# 
# ======================================================================================
# Serializer Site Content Settings (Sections)
# ======================================================================================
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ["id"]

    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=Content, rules=CONTENT_RULES)
    # ===============================================================================================================
# ======================================================================================
# 
# 
# ======================================================================================
# Serializer Faqs
# ======================================================================================
class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'
        read_only_fields = ["id"]

    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=Faq, rules=FAQ_RULES)
    # ===============================================================================================================  
# ======================================================================================



# ======================================================================================
# Serializer Site Content Settings , Platform Settings, Faqs - Public 
# ======================================================================================
class PublicPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformSettings
        fields = '__all__'

class PublicContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class PublicFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'
# ======================================================================================





