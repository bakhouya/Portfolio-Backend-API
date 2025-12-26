from django.db import models
import uuid

# ======================================================================================
# Service Model
# ======================================================================================
class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name="Title")
    image = models.ImageField(upload_to="services/", blank=True, null=True, verbose_name="Image")
    description = models.TextField(verbose_name="Description")
    color = models.CharField(max_length=7, default='#4A90E2', verbose_name="Color")
    status = models.BooleanField(default=True, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['created_at']

    def __str__(self):
        return self.title
# ======================================================================================

