from django.db import models
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

# =====================================================================
# ExperienceType Model
# =====================================================================
class EducationType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, verbose_name="Title", unique=True)
    status = models.BooleanField(default=True, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Education Type"
        verbose_name_plural = "Education Types"
        ordering = ["title"]

    def __str__(self):
        return self.title

    @classmethod
    def default_types(modelClass):
        if not modelClass.objects.exists():
            default_types = [
                {'title': 'High School'},
                {'title': 'Diploma'},
                {'title': 'Bachelor'},
                {'title': 'Master'},
                {'title': 'Phd'},
                {'title': 'Certificate'}
            ]           
            for type_data in default_types:
                modelClass.objects.create(**type_data)
            
            return True
        return False
# =====================================================================
# 
# 
# =====================================================================
# Education Model
# =====================================================================
class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # "مجال الدراسة"
    field_of_study = models.CharField(max_length=200, verbose_name="field of study")
    # "المؤسسة التعليمية"
    institution = models.CharField(max_length=200, verbose_name="University")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Location")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_current = models.BooleanField(default=False, verbose_name="Current")
    logo = models.ImageField(upload_to='education/', blank=True, null=True, verbose_name="Logo University")
    status = models.BooleanField(default=False, verbose_name="Published")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="educations")
    type = models.ForeignKey(EducationType, on_delete=models.CASCADE, related_name="educations")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.field_of_study
    
# =====================================================================
