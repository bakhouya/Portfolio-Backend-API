
from rest_framework import  permissions, serializers
from utils.validator import DynamicValidator
from django.core.exceptions import ValidationError


# ========================================================================================= 
# if the new value is a new uploaded file
# ========================================================================================= 
def is_new_file(new_file, old_file):
    if not new_file:
        return False
    from django.core.files.uploadedfile import UploadedFile
    return isinstance(new_file, UploadedFile)
# ========================================================================================= 

# ========================================================================================= 
# safely delete a file field
# ========================================================================================= 
def safe_delete_file(file_field):
    if file_field and hasattr(file_field, "delete"):
        try:
            file_field.delete(save=False)
        except:
            pass

# ========================================================================================= 

# ========================================================================================= 
# handle file update logic
# ========================================================================================= 
def handle_file_update(new_file, old_file):
    if is_new_file(new_file, old_file) and old_file:
        safe_delete_file(old_file)
# ========================================================================================= 


# =====================================================================================================================
# A custom permission used to verify that the current user
# is the same user associated with the object (the true owner of the data).
# Purpose:
# - Prevent any user from modifying or accessing an object they do not own.
# - Ensure that sensitive operations (modify/delete) are performed only by the owner.
# How it works:
# - The user associated with the object (obj.user) is compared
# with the user who submitted the request (request.user).
# Result:
# - Access is granted if the user is the owner.
# - The request is denied if the user is not.
# =====================================================================================================================
class IsOwnerAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
# =====================================================================================================================




# =====================================================================================================================
# handler function to validate incoming data for serializers
# =====================================================================================================================
def validation_handler(serializer_class, model_class, rules, data, instance=None):
    validator = DynamicValidator(model_class, instance=instance)
    is_update = instance is not None   
    try:
        cleaned_data = validator.validate(data, rules, is_update=is_update)
    except ValidationError as e:
        raise serializers.ValidationError(e.message_dict)   
    return cleaned_data

def hanlde_validator(model_class, rules):
    def to_internal_value(self, data):
        cleaned_data = validation_handler( 
            serializer_class=self.__class__,
            model_class=model_class,
            rules=rules,
            data=data,
            instance=self.instance
        )
        return super(self.__class__, self).to_internal_value(cleaned_data)
    
    return to_internal_value
# =====================================================================================================================

