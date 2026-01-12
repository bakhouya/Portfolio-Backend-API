
from contacts.rules import CONTACT_RULES
from rest_framework import serializers
from utils.helpers import hanlde_validator
from .models import Contact



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
   
    # ===============================================================================================================
    # Custom validator handlier
    # ===============================================================================================================
    to_internal_value = hanlde_validator(model_class=Contact, rules=CONTACT_RULES)
    # ===============================================================================================================















