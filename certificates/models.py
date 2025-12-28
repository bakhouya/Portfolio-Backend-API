from django.db import models
from skills.models import Skill
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

# ================================================================================
# Certificate Model
# ================================================================================
class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    issuing_organization = models.CharField(max_length=200, verbose_name="Issuing Organization")
    # تاريخ الإصدار
    issue_date = models.DateField(verbose_name="Issue Date")
    # تاريخ الانتهاء
    expiration_date = models.DateField(blank=True, null=True, verbose_name="Expiration Date")
    # رقم الاعتماد
    credential_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Credential ID")
    credential_url = models.URLField(blank=True, null=True, verbose_name="Credential URL")
    image = models.ImageField(upload_to='certificates/', blank=True, null=True, verbose_name="Image")
    skills = models.ManyToManyField(Skill, blank=True, related_name="certificates")
    status = models.BooleanField(default=False, verbose_name="Published")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificates")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
        ordering = ['-issue_date']

    def __str__(self):
        return self.title
# ================================================================================
