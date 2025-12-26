from django.db import models
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()


# =====================================================================
# ExperienceType Model
# =====================================================================
class ExperienceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, verbose_name="Title", unique=True)
    status = models.BooleanField(default=True, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Experience Type"
        verbose_name_plural = "Experience Types"
        ordering = ['title']

    def __str__(self):
        return self.title
    
    @classmethod
    def default_types(modelClass):
        if not modelClass.objects.exists():
            default_types = [
                {'title': 'Full Time'},
                {'title': 'Part Time'},
                {'title': 'Contract'},
                {'title': 'Freelance'},
                {'title': 'internship'}
            ]           
            for type_data in default_types:
                modelClass.objects.create(**type_data)
            
            return True
        return False
# =====================================================================
# 
# 
# =====================================================================
# Experience Model
# =====================================================================
class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name="Job Experience")
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name="Company")
    description = models.TextField(verbose_name="Description")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_current = models.BooleanField(default=False, verbose_name="Current")
    logo = models.ImageField(upload_to='experiences/', blank=True, null=True, verbose_name="Logo")
    status = models.BooleanField(default=True, verbose_name="Published")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="experiences")
    type = models.ForeignKey(ExperienceType, on_delete=models.CASCADE, related_name="experiences")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ['-start_date']
        
    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title  
# =====================================================================




