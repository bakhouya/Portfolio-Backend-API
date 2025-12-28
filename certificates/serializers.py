
# =====================================================================================================================
# imports 
# =====================================================================================================================
from certificates.rules import CERTIFICATE_RULES
from rest_framework import serializers
from utils.helpers import handle_file_update, hanlde_validator
from .models import Certificate
from skills.models import Skill
# =====================================================================================================================



# =====================================================================================================================
# CertificateSkillsSerializer for get skills certificate
# =====================================================================================================================
class CertificateSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill 
        fields = ["id", "title", "icon"]
        read_only_fields = ["id", "title", "icon"]
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# CertificateSerializer for admin handler DRUD certificates (get, create, update, delete)
# =====================================================================================================================
class CertificateSerializer(serializers.ModelSerializer):
    skills = serializers.ListField(child=serializers.UUIDField(), write_only=True)
    certificate_skills = CertificateSkillsSerializer(many=True, read_only=True, source='skills')

    class Meta:
        model = Certificate
        fields = ['id', 'title', 'description', 'issuing_organization', 
                 'issue_date', 'expiration_date', 'credential_id', 
                 'credential_url', 'image', 'status', 'skills', 'certificate_skills',
                 'created_at', 'updated_at', 'user']
        read_only_fields = ["id", "created_at", "updated_at", "user", "certificate_skills"]

    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=Certificate, rules=CERTIFICATE_RULES)
    # ===============================================================================================================
    # 
    # 
    # ===============================================================================================================
    # ===============================================================================================================
    def create(self, data):
        skills = data.pop('skills', [])
        certificate = Certificate.objects.create(**data)
        certificate.skills.add(*skills)       
        return certificate
    # ===============================================================================================================
    # 
    # 
    # ===============================================================================================================
    # handler update to manage file fields 
    # if files are updated, old files are deleted from the storage "media/"
    # ===============================================================================================================
    def update(self, instance, data):
        skills_data = data.pop('skills', None)
        if "image" in data:
            handle_file_update(data.get("image"), instance.image)
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance.save()

        if skills_data is not None:
            instance.skills.set(skills_data)
        
        return instance
    # ===============================================================================================================
# =====================================================================================================================
# 
# 
# =====================================================================================================================
# PublicCertificaleSerializer for public get active certificates
# =====================================================================================================================
class PublicCertificaleSerializer(serializers.ModelSerializer):
    certificate_skills = CertificateSkillsSerializer(many=True, read_only=True, source='skills')
    class Meta:
        model = Certificate
        fields = "__all__"
# =====================================================================================================================

